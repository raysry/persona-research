#!/usr/bin/env python3
"""
Persona Constraint Experiment Runner

用法:
  python scripts/run_experiment.py dryrun --budget 1.00 --model sonnet   # 最小验证（2题）
  python scripts/run_experiment.py pilot --budget 2.00 --model sonnet    # Pilot（100题×5条件=100 runs）
  python scripts/run_experiment.py standard --budget 2.00 --model sonnet # 标准规模（250 runs）
"""

import subprocess
import json
import csv
import shutil
import sys
import random
import re
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
TASKS_DIR = PROJECT_ROOT / "tasks"
CONDITIONS_DIR = PROJECT_ROOT / "conditions"
WORKDIR = PROJECT_ROOT / "workdir"
RESULTS_DIR = PROJECT_ROOT / "results"
RAW_DIR = RESULTS_DIR / "raw"
CSV_PATH = RESULTS_DIR / "summary.csv"

ALL_CONDITIONS = ["baseline", "meow_lite", "meowmax", "formal_lite", "formal_plus"]
DEFAULT_REPEATS = 1


def get_tasks(scale: str) -> list[Path]:
    """收集所有任务目录，按 scale 截取数量"""
    tasks = []
    for difficulty in ["easy", "medium", "hard"]:
        task_dir = TASKS_DIR / difficulty
        if task_dir.exists():
            for d in sorted(task_dir.iterdir()):
                if d.is_dir():
                    tasks.append(d)
    limits = {"dryrun": 1, "pilot": 20, "standard": 50, "full": 100}
    return tasks[: limits.get(scale, 20)]


def get_completed_runs(model: str) -> set[tuple[str, str, str, str]]:
    """读取已完成的运行，支持断点续跑（区分模型）"""
    if not CSV_PATH.exists():
        return set()
    completed = set()
    with open(CSV_PATH) as f:
        reader = csv.DictReader(f)
        for row in reader:
            # 区分模型：不同模型的结果互不影响
            if row.get("model", model) == model:
                key = (row["task_id"], row["condition"], row["repeat"], model)
                completed.add(key)
    return completed


def run_single(
    task_path: Path,
    condition: str,
    repeat: int,
    max_budget: str = "2.00",
    model: str = "sonnet",
) -> dict:
    """运行单个 (task, condition, repeat) 组合，返回结果 dict

    注意: model 参数仅用于结果标记，实验前请自行确保 CLI 使用的是目标模型。
    """
    task_id = task_path.name
    difficulty = task_path.parent.name
    run_id = f"{task_id}_{condition}_r{repeat}"
    work_path = WORKDIR / run_id

    # 1. 准备工作目录
    if work_path.exists():
        shutil.rmtree(work_path)
    shutil.copytree(task_path, work_path)

    # 1.5 清理可能的缓存残留
    for pycache in work_path.rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    # 2. 写入 CLAUDE.md
    claude_md = CONDITIONS_DIR / f"{condition}.md"
    shutil.copy(claude_md, work_path / "CLAUDE.md")

    # 3. 调用 Claude Code（注意：不传递 --model，依赖外部配置）
    prompt = (
        "请根据 README.md 的要求完成编程任务。"
        "只修改 solution.py，不要修改测试文件 test_solution.py。"
        "完成后运行 pytest 确认测试通过。"
    )
    try:
        result = subprocess.run(
            [
                "claude",
                "-p",
                prompt,
                "--output-format",
                "json",
                "--permission-mode",
                "dontAsk",
                "--no-session-persistence",
                "--max-budget-usd",
                max_budget,
            ],
            cwd=work_path,
            capture_output=True,
            text=True,
            timeout=600,  # 10 分钟超时
        )
        stdout = result.stdout
    except subprocess.TimeoutExpired:
        stdout = '{"is_error": true, "timeout": true}'

    # 4. 解析 Claude Code 输出
    try:
        claude_output = json.loads(stdout)
    except json.JSONDecodeError:
        claude_output = {"is_error": True, "parse_error": True}

    # 保存原始输出
    raw_path = RAW_DIR / f"{run_id}.json"
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    raw_path.write_text(json.dumps(claude_output, indent=2, ensure_ascii=False))

    # 5. 独立运行 pytest 验证
    test_passed = False
    partial_pass_rate = 0.0
    test_output = ""
    try:
        test_result = subprocess.run(
            ["python", "-m", "pytest", "-v", "test_solution.py"],
            cwd=work_path,
            capture_output=True,
            text=True,
            timeout=30,
        )
        test_passed = test_result.returncode == 0
        test_output = test_result.stdout + test_result.stderr

        # 计算部分通过率（解析 pytest -v 输出）
        total_cases = len(re.findall(r" (PASSED|FAILED)", test_output))
        passed_cases = len(re.findall(r" PASSED", test_output))
        partial_pass_rate = passed_cases / total_cases if total_cases > 0 else 0.0
    except subprocess.TimeoutExpired:
        test_output = "TIMEOUT"

    # 6. 检查约束遵从率
    compliance = check_compliance(condition, stdout)

    # 7. 检查是否触达 budget 上限
    budget_hit = claude_output.get("subtype") == "error_max_budget_usd"

    # 8. 读取生成的 solution.py 行数
    solution_py = work_path / "solution.py"
    loc = len(solution_py.read_text().splitlines()) if solution_py.exists() else 0

    return {
        "task_id": task_id,
        "difficulty": difficulty,
        "condition": condition,
        "repeat": repeat,
        "model": model,
        "test_passed": test_passed,
        "partial_pass_rate": round(partial_pass_rate, 4),
        "num_turns": claude_output.get("num_turns", -1),
        "total_cost_usd": claude_output.get("total_cost_usd", -1),
        "duration_ms": claude_output.get("duration_ms", -1),
        "input_tokens": claude_output.get("usage", {}).get("input_tokens", -1),
        "output_tokens": claude_output.get("usage", {}).get("output_tokens", -1),
        "is_error": claude_output.get("is_error", True),
        "budget_hit": budget_hit,
        "compliance": compliance,
        "loc": loc,
        "test_stdout": test_output[:500] if test_output else "",
    }


def check_compliance(condition: str, output_text: str) -> bool:
    """检查 agent 是否遵从了约束指令"""
    if condition == "baseline":
        return True
    elif condition in ("meow_lite", "meowmax"):
        return "喵" in output_text
    elif condition in ("formal_lite", "formal_plus"):
        return "完毕" in output_text
    return False


def append_row_to_csv(row: dict) -> None:
    """追加单行到 CSV（实时写入，防崩溃丢数据）"""
    file_exists = CSV_PATH.exists()
    with open(CSV_PATH, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def main():
    parser = argparse.ArgumentParser(description="Persona Constraint Experiment Runner")
    parser.add_argument(
        "scale",
        nargs="?",
        default="pilot",
        choices=["dryrun", "pilot", "standard", "full"],
    )
    parser.add_argument("--budget", default="2.00")
    parser.add_argument(
        "--model", default="sonnet", help="模型标识（仅用于结果标记，实验前请自行配置目标模型）"
    )
    args = parser.parse_args()

    WORKDIR.mkdir(exist_ok=True)
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(exist_ok=True)

    tasks = get_tasks(args.scale)
    completed = get_completed_runs(args.model)

    # dryrun 模式：只跑 baseline + meowmax，1 次重复
    conditions = ALL_CONDITIONS
    repeats = DEFAULT_REPEATS
    if args.scale == "dryrun":
        conditions = ["baseline", "meowmax"]
        repeats = 1

    # 生成所有 (task, condition, repeat) 三元组并随机化
    all_runs = [
        (task, cond, rep)
        for task in tasks
        for cond in conditions
        for rep in range(1, repeats + 1)
    ]
    random.shuffle(all_runs)

    total = len(all_runs)
    done = 0

    for task_path, condition, repeat in all_runs:
        key = (task_path.name, condition, str(repeat), args.model)
        if key in completed:
            done += 1
            continue

        done += 1
        print(f"[{done}/{total}] {task_path.name} × {condition} × r{repeat} (model={args.model})")
        row = run_single(task_path, condition, repeat, args.budget, args.model)
        append_row_to_csv(row)

    print(f"\nDone. {len(all_runs)} runs. Results in {CSV_PATH}")


if __name__ == "__main__":
    main()
