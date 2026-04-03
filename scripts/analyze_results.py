#!/usr/bin/env python3
"""
Persona Constraint Experiment — Analysis & Figures

用法:
  cd persona-research
  python scripts/analyze_results.py            # 输出统计 + 生成图表
  python scripts/analyze_results.py --no-plots # 仅输出统计
"""

import argparse
import os
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats

# ── 全局配置 ────────────────────────────────────────────────
RESULTS_CSV = "results/summary.csv"
FIGURES_DIR = "results/figures"

# 条件显示顺序和缩写标签
CONDITION_ORDER = ["baseline", "meow_lite", "meowmax", "formal_lite", "formal_plus"]
CONDITION_LABELS = {
    "baseline": "Baseline",
    "meow_lite": "Meow Lite",
    "formal_lite": "Formal Lite",
    "formal_plus": "Formal Plus",
    "meowmax": "MeowMax",
}
DIFFICULTY_ORDER = ["easy", "medium", "hard"]

# Planned contrasts: (cond_a, cond_b, label, question)
PLANNED_CONTRASTS = [
    ("baseline", "formal_lite", "C1", "后缀指令的纯粹成本"),
    ("meow_lite", "formal_lite", "C2", "persona 语义效应"),
    ("meowmax", "formal_plus", "C3", "完整 persona vs 纯格式约束"),
    ("meowmax", "meow_lite", "C4", "身份重定义增量成本"),
]

# 样式
sns.set_theme(style="whitegrid", font_scale=1.05)
PALETTE = sns.color_palette("Set2", len(CONDITION_ORDER))
COND_COLORS = dict(zip(CONDITION_ORDER, PALETTE))


# ── 数据加载 ────────────────────────────────────────────────
def load_data() -> pd.DataFrame:
    df = pd.read_csv(RESULTS_CSV)
    df["condition"] = pd.Categorical(df["condition"], categories=CONDITION_ORDER, ordered=True)
    df["difficulty"] = pd.Categorical(df["difficulty"], categories=DIFFICULTY_ORDER, ordered=True)
    return df


# ── 统计检验 ────────────────────────────────────────────────
def omnibus_tests(df: pd.DataFrame) -> dict:
    """整体检验：卡方 (test_passed) + Kruskal-Wallis (partial_pass_rate)"""
    # 卡方检验
    ct = pd.crosstab(df["condition"], df["test_passed"])
    chi2, p_chi2, dof, _ = stats.chi2_contingency(ct)

    # Kruskal-Wallis
    groups = [g["partial_pass_rate"].values for _, g in df.groupby("condition", observed=True)]
    H, p_kw = stats.kruskal(*groups)

    return {"chi2": chi2, "chi2_dof": dof, "chi2_p": p_chi2, "kw_H": H, "kw_p": p_kw}


def planned_contrast_tests(df: pd.DataFrame) -> pd.DataFrame:
    """四组 planned contrasts: Mann-Whitney U + Fisher exact"""
    rows = []
    for cond_a, cond_b, label, question in PLANNED_CONTRASTS:
        a = df[df.condition == cond_a]
        b = df[df.condition == cond_b]

        # Mann-Whitney U on partial_pass_rate
        U, p_mw = stats.mannwhitneyu(
            a["partial_pass_rate"], b["partial_pass_rate"], alternative="two-sided"
        )
        n1, n2 = len(a), len(b)
        r_rb = 1 - (2 * U) / (n1 * n2)  # rank-biserial effect size

        # Fisher exact on test_passed
        ct = pd.DataFrame(
            {
                "pass": [a["test_passed"].sum(), b["test_passed"].sum()],
                "fail": [(~a["test_passed"]).sum(), (~b["test_passed"]).sum()],
            },
            index=[cond_a, cond_b],
        )
        OR, p_fisher = stats.fisher_exact(ct.values)

        delta = a["partial_pass_rate"].mean() - b["partial_pass_rate"].mean()

        rows.append({
            "contrast": label,
            "question": question,
            "cond_a": CONDITION_LABELS[cond_a],
            "cond_b": CONDITION_LABELS[cond_b],
            "delta": delta,
            "U": U,
            "p_mw": p_mw,
            "r_rb": r_rb,
            "OR": OR,
            "p_fisher": p_fisher,
        })
    return pd.DataFrame(rows)


def efficiency_kw_tests(df: pd.DataFrame) -> pd.DataFrame:
    """效率指标的 Kruskal-Wallis 检验"""
    metrics = ["num_turns", "total_cost_usd", "output_tokens", "duration_ms"]
    labels = ["对话轮次", "API 成本", "输出 token 数", "端到端耗时"]
    rows = []
    for metric, label in zip(metrics, labels):
        groups = [g[metric].values for _, g in df.groupby("condition", observed=True)]
        H, p = stats.kruskal(*groups)
        rows.append({"metric": label, "H": H, "p": p})
    return pd.DataFrame(rows)


# ── 描述统计 ────────────────────────────────────────────────
def descriptive_stats(df: pd.DataFrame) -> dict:
    """生成论文需要的所有描述统计"""
    result = {}

    # 按条件汇总
    by_cond = df.groupby("condition", observed=True).agg(
        n=("test_passed", "size"),
        pass_count=("test_passed", "sum"),
        pass_rate=("test_passed", "mean"),
        ppr_mean=("partial_pass_rate", "mean"),
        ppr_std=("partial_pass_rate", "std"),
        compliance_rate=("compliance", "mean"),
        turns_median=("num_turns", "median"),
        cost_median=("total_cost_usd", "median"),
        tokens_median=("output_tokens", "median"),
        duration_median=("duration_ms", "median"),
        loc_median=("loc", "median"),
    )
    result["by_condition"] = by_cond

    # 按难度 × 条件
    by_diff = df.pivot_table(
        values="test_passed", index="difficulty", columns="condition", aggfunc="mean",
        observed=True,
    )
    result["by_difficulty"] = by_diff

    # 失败案例
    failures = df[df["test_passed"] == False][
        ["task_id", "condition", "partial_pass_rate"]
    ].sort_values(["task_id", "condition"])
    result["failures"] = failures

    return result


# ── 图表 ────────────────────────────────────────────────────
def _save(fig, name: str):
    path = os.path.join(FIGURES_DIR, name)
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  saved: {path}")


def plot_pass_rate(df: pd.DataFrame):
    """Fig 1: 各条件测试通过率 (grouped bar)"""
    fig, ax = plt.subplots(figsize=(8, 4.5))
    by_cond = df.groupby("condition", observed=True)["test_passed"].mean()
    labels = [CONDITION_LABELS[c] for c in CONDITION_ORDER]
    values = [by_cond[c] for c in CONDITION_ORDER]
    colors = [COND_COLORS[c] for c in CONDITION_ORDER]

    bars = ax.bar(labels, values, color=colors, edgecolor="white", width=0.6)
    for bar, v in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, v + 0.01,
                f"{v:.0%}", ha="center", va="bottom", fontsize=11)

    ax.set_ylim(0, 1.15)
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(1.0))
    ax.set_ylabel("Test Pass Rate")
    ax.set_title("Test Pass Rate by Condition")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    _save(fig, "pass_rate_by_condition.png")


def plot_pass_rate_by_difficulty(df: pd.DataFrame):
    """Fig 2: 难度 × 条件 通过率热力图"""
    pivot = df.pivot_table(
        values="test_passed", index="difficulty", columns="condition", aggfunc="mean",
        observed=True,
    )
    pivot = pivot[CONDITION_ORDER]
    pivot.columns = [CONDITION_LABELS[c] for c in pivot.columns]

    fig, ax = plt.subplots(figsize=(8, 3.5))
    sns.heatmap(
        pivot, annot=True, fmt=".0%", cmap="YlGn", vmin=0.5, vmax=1.0,
        linewidths=0.5, ax=ax, cbar_kws={"format": mticker.PercentFormatter(1.0)}
    )
    ax.set_title("Test Pass Rate by Difficulty × Condition")
    ax.set_ylabel("")
    ax.set_xlabel("")
    _save(fig, "pass_rate_by_difficulty.png")


def plot_partial_pass_distribution(df: pd.DataFrame):
    """Fig 3: 用例通过比例的分布 (strip + box)"""
    fig, ax = plt.subplots(figsize=(8, 4.5))
    df_plot = df.copy()
    df_plot["cond_label"] = df_plot["condition"].map(CONDITION_LABELS)

    sns.boxplot(
        data=df_plot, x="cond_label", y="partial_pass_rate", hue="cond_label",
        order=[CONDITION_LABELS[c] for c in CONDITION_ORDER],
        hue_order=[CONDITION_LABELS[c] for c in CONDITION_ORDER],
        palette=COND_COLORS.values(), width=0.5, fliersize=0, legend=False, ax=ax,
    )
    sns.stripplot(
        data=df_plot, x="cond_label", y="partial_pass_rate",
        order=[CONDITION_LABELS[c] for c in CONDITION_ORDER],
        color="0.3", size=4, alpha=0.6, jitter=0.15, ax=ax,
    )
    ax.set_ylim(-0.05, 1.15)
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(1.0))
    ax.set_ylabel("Partial Pass Rate")
    ax.set_xlabel("")
    ax.set_title("Partial Pass Rate Distribution by Condition")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    _save(fig, "partial_pass_distribution.png")


def plot_compliance(df: pd.DataFrame):
    """Fig 4: 约束遵从率"""
    fig, ax = plt.subplots(figsize=(8, 4.5))
    by_cond = df.groupby("condition", observed=True)["compliance"].mean()
    labels = [CONDITION_LABELS[c] for c in CONDITION_ORDER]
    values = [by_cond[c] for c in CONDITION_ORDER]
    colors = [COND_COLORS[c] for c in CONDITION_ORDER]

    bars = ax.bar(labels, values, color=colors, edgecolor="white", width=0.6)
    for bar, v in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, v + 0.01,
                f"{v:.0%}", ha="center", va="bottom", fontsize=11)

    ax.set_ylim(0, 1.15)
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(1.0))
    ax.set_ylabel("Compliance Rate")
    ax.set_title("Constraint Compliance Rate by Condition")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    _save(fig, "compliance_by_condition.png")


def plot_efficiency(df: pd.DataFrame):
    """Fig 5: 效率指标 (2x2 box plot)"""
    metrics = [
        ("num_turns", "Dialogue Turns"),
        ("total_cost_usd", "API Cost (USD)"),
        ("output_tokens", "Output Tokens"),
        ("duration_ms", "Duration (ms)"),
    ]
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    axes = axes.flatten()

    df_plot = df.copy()
    df_plot["cond_label"] = df_plot["condition"].map(CONDITION_LABELS)
    order = [CONDITION_LABELS[c] for c in CONDITION_ORDER]

    for ax, (col, title) in zip(axes, metrics):
        sns.boxplot(
            data=df_plot, x="cond_label", y=col, hue="cond_label",
            order=order, hue_order=order,
            palette=COND_COLORS.values(), width=0.5, fliersize=3, legend=False, ax=ax,
        )
        ax.set_title(title)
        ax.set_xlabel("")
        ax.tick_params(axis="x", rotation=25)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    fig.suptitle("Efficiency Metrics by Condition", fontsize=14, y=1.01)
    fig.tight_layout()
    _save(fig, "efficiency_metrics.png")


# ── 主流程 ──────────────────────────────────────────────────
def print_section(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-plots", action="store_true", help="跳过图表生成")
    args = parser.parse_args()

    df = load_data()
    print(f"Loaded {len(df)} runs: {df['task_id'].nunique()} tasks × {df['condition'].nunique()} conditions")
    print(f"Errors: {df['is_error'].sum()}, Budget hits: {df['budget_hit'].sum()}")

    # ── 描述统计 ──
    desc = descriptive_stats(df)

    print_section("测试通过率 & 用例通过比例（按条件）")
    tbl = desc["by_condition"][["n", "pass_count", "pass_rate", "ppr_mean", "ppr_std"]]
    tbl.columns = ["N", "Pass", "Pass Rate", "PPR Mean", "PPR Std"]
    print(tbl.round(3).to_string())

    print_section("测试通过率（按难度 × 条件）")
    print(desc["by_difficulty"].round(3).to_string())

    print_section("效率指标中位数（按条件）")
    tbl = desc["by_condition"][["turns_median", "cost_median", "tokens_median", "duration_median", "loc_median"]]
    tbl.columns = ["Turns", "Cost ($)", "Tokens", "Duration (ms)", "LOC"]
    print(tbl.round(3).to_string())

    print_section("约束遵从率（按条件）")
    tbl = desc["by_condition"][["compliance_rate"]]
    tbl.columns = ["Compliance"]
    print(tbl.round(3).to_string())

    print_section("失败案例")
    if len(desc["failures"]) == 0:
        print("(无失败案例)")
    else:
        print(desc["failures"].to_string(index=False))

    # ── 统计检验 ──
    print_section("整体检验")
    omni = omnibus_tests(df)
    print(f"测试通过率 χ²({omni['chi2_dof']}) = {omni['chi2']:.3f}, p = {omni['chi2_p']:.3f}")
    print(f"用例通过比例 Kruskal-Wallis H = {omni['kw_H']:.3f}, p = {omni['kw_p']:.3f}")

    print_section("Planned Contrasts")
    contrasts = planned_contrast_tests(df)
    for _, row in contrasts.iterrows():
        print(f"{row['contrast']} ({row['question']})")
        print(f"  {row['cond_a']} vs {row['cond_b']}")
        print(f"  Δ = {row['delta']:+.3f}, U = {row['U']:.1f}, p = {row['p_mw']:.3f}, r = {row['r_rb']:.3f}")
        print(f"  Fisher exact: OR = {row['OR']:.2f}, p = {row['p_fisher']:.3f}")
        print()

    print_section("效率指标 Kruskal-Wallis")
    eff_kw = efficiency_kw_tests(df)
    for _, row in eff_kw.iterrows():
        print(f"{row['metric']}: H = {row['H']:.3f}, p = {row['p']:.3f}")

    # ── 图表 ──
    if not args.no_plots:
        print_section("生成图表")
        os.makedirs(FIGURES_DIR, exist_ok=True)
        plot_pass_rate(df)
        plot_pass_rate_by_difficulty(df)
        plot_partial_pass_distribution(df)
        plot_compliance(df)
        plot_efficiency(df)
        print(f"\n所有图表已保存到 {FIGURES_DIR}/")


if __name__ == "__main__":
    main()
