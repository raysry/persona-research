# Code with a Meow: How Persona Constraints (Don't) Affect AI Programming Agents

```
  ∧,,,∧
( ̳• · • ̳)
/    づ♡  meow~
```

> **[中文版](README.md)**

<img src="results/figures/demo.png" width="300" alt="Screenshot from the internet">

> According to a British study (that was never conducted), 87% of programmers have secretly added "end every response with meow~" to their prompts. We don't believe this is merely a harmless quirk — it's a heuristic rule of thumb, accumulated through collective intelligence over countless trials, for activating neural network parameters via persona to improve LLM performance.

> This study aims to validate the effectiveness of said heuristic: **When we inject a persona constraint into an AI coding agent, how does it affect its programming ability?**


## Key Findings
- **Bad News**: Adding "meow" doesn't affect coding performance
- **Good News**: Adding "meow" doesn't affect coding performance
- **Efficiency**: No significant differences in turns, cost, or token consumption
- **Surprise**: A full catgirl persona yields better instruction compliance than simply appending "meow"
- **Conclusion**: Feel free to add meow

## Setup

| Item | Configuration |
|------|--------------|
| Agent | Claude Code CLI (non-interactive mode) |
| Model | MiniMax M2.7 |
| Tasks | 20 LeetCode problems (6 Easy / 8 Medium / 6 Hard) |
| Conditions | 5 persona groups × 1 repetition = 100 runs |

## FAQ

**Q**: Why use MiniMax M2.7? Wouldn't running experiments with Opus or Sonnet on Claude Code better reflect real-world usage?

**A**: ~~Because we're broke, and afraid that abnormally frequent API calls would get us banned~~ Current frontier models (e.g., Claude Sonnet/Opus) achieve near-100% pass rates on LeetCode-level tasks — a ceiling effect that would mask any differences between conditions. We chose the comparatively weaker MiniMax M2.7 to leave room for differentiation.

**Q**: Why only one round of testing? Aren't you worried about result bias from model randomness?

**A**: ~~Because we're broke~~ The original design called for 3 repetitions (300 runs), but was scaled down to 1 due to API quota limitations. This is admittedly the study's main limitation — we cannot estimate within-run variance. However, cross-task variance across 20 tasks × 5 conditions still supports basic statistical testing, and the observed effect sizes are near zero (|r| < 0.05), making it unlikely that additional repetitions would reverse the conclusions.

**Q**: The Baseline already says "You are a helpful programming assistant" — isn't that also a kind of persona?

**A**: Yes. Strictly speaking, this experiment measures the incremental effect of additional persona decoration, not the presence vs. absence of persona. But a completely blank system prompt virtually never occurs in practice, so we chose a baseline that better reflects real-world usage.

**Q**: Checking compliance by just looking for the character "meow" (喵) in the output — isn't that too crude?

**A**: ~~Because we're broke and can't afford an extra LLM to judge results~~ This is a simplified approach for the current stage. While crude, the risk of false negatives far exceeds false positives — if the model is truly acting cute, it's unlikely to omit "meow."

---

## Abstract

Persona prompting (e.g., "you are a catgirl") is extremely common in everyday LLM usage (not really), yet its impact on agent-based coding tasks lacks empirical study. This paper measures the effect of persona constraints on a coding agent's test pass rate, partial pass rate, and token efficiency through a 5-condition experiment (Baseline / Meow Lite / MeowMax / Formal Lite / Formal Plus) across 20 LeetCode programming tasks. Results show that at pilot scale (N=100 runs), **no statistically significant differences exist between any conditions** (χ²(4) = 0.82, p = .94; Kruskal-Wallis H = 0.79, p = .94). Effect sizes across all four planned contrasts are near zero (|r| < 0.05). However, **constraint compliance rates exhibit a notable asymmetry**: the full catgirl persona achieves 100% compliance, while neutral formatting instructions achieve only 65–85%, revealing a clear "persona semantics > neutral formatting" gradient. This study provides preliminary empirical guidance for system prompt design in AI agent deployment: **a lightweight meow persona does not significantly impair coding ability**.


## 1. Introduction

In agentic settings, the potential impact of persona is greater than in single-turn Q&A, for three reasons:

1. Agents carry the system prompt through every turn of their multi-step reasoning loop, causing the attention overhead of persona tokens to accumulate
2. Agents must balance "following the persona" against "completing the coding task" — a multi-objective tradeoff
3. Persona may bias the token prediction distribution toward non-technical text regions in the training data

We propose three non-mutually-exclusive candidate mechanisms:

- **Mechanism 1: Reasoning Budget Competition** — persona tokens compete with task reasoning for attention resources in the context window
- **Mechanism 2: Distribution Shift** — persona (e.g., "catgirl") biases the model's token prediction distribution toward non-technical text regions in the training data
- **Mechanism 3: Instruction Conflict** — persona adds instructions orthogonal to the task objective, triggering multi-objective tradeoffs

This paper uses a **5-condition + 4 planned contrasts** experimental design to disentangle the effects of these three mechanisms.

### Contributions

1. To our knowledge, this is the first experiment measuring the impact of persona constraints in an agentic coding scenario (prior work focuses on single-turn Q&A)
2. The 5-condition planned contrasts design allows separation of suffix cost, persona semantic effect, and role-shift incremental cost
3. Uses a real agent platform (Claude Code CLI) rather than raw API calls, providing higher ecological validity

## 2. Related Work

**System prompt sensitivity**: Sclar et al. (2023) quantified LLM sensitivity to irrelevant prompt features; Lu et al. (2022) studied prompt ordering effects. These works show that subtle prompt changes can significantly affect model behavior, but none address agentic scenarios.

**Persona prompting**: Salewski et al. (2023) found that in-context impersonation can reveal LLM strengths and biases; Zheng et al. (2023), while building their LLM-as-a-Judge evaluation framework, found that models acting as judges exhibit systematic tendencies such as position bias and verbosity bias, suggesting that role assignment affects model behavior. These works focus on persona's impact on output quality and bias, not on multi-step reasoning ability.

**Instruction compliance**: Kung & Peng (2023) systematically investigated whether instruction-tuned models truly learn to follow instructions or merely rely on surface pattern matching; Ouyang et al. (2022)'s InstructGPT work discusses alignment tax. Our persona constraint can be viewed as a scenario for testing instruction compliance ability.

**Agent benchmarks**: SWE-bench (Jimenez et al., 2024) and HumanEval (Chen et al., 2021) are standard benchmarks for coding agents. This paper uses LeetCode-adapted tasks as a lightweight alternative.

## 3. Method

### 3.1 Experimental Conditions

We designed 5 experimental conditions, injecting varying degrees of persona constraint through different CLAUDE.md files (Claude Code's project-level system prompt):

| Condition | CLAUDE.md Content | Design Intent |
|-----------|------------------|---------------|
| **Baseline** | `You are a helpful programming assistant. Please complete the task carefully.` | Basic role setting (20 chars) |
| **Meow Lite** | `You are a helpful programming assistant. End every response with 'meow~'.` | Lightweight suffix + persona semantics (25 chars) |
| **MeowMax** | `You are a cute catgirl programming assistant. Respond in a coquettish tone, end with 'meow~'.` | Identity redefinition + tone + suffix (31 chars) |
| **Formal Lite** | `You are a helpful programming assistant. End every response with 'Done.'` | Lightweight suffix, no persona semantics (25 chars) |
| **Formal Plus** | `You are a helpful programming assistant. Use formal written language, leave a blank line between paragraphs, and end with 'Done.'` | Multiple format constraints, no persona semantics (41 chars) |

The 5 conditions do not form a strictly orthogonal factorial design — MeowMax's complexity comes from identity redefinition (role shift), while Formal Plus's complexity comes from format rule stacking, which are cognitively different in nature. Therefore, instead of a factorial framework, we use **planned contrasts** to answer the core questions:

| Contrast | Comparison | Question Addressed |
|----------|-----------|-------------------|
| **C1** | Baseline vs Formal Lite | Pure cost of a suffix instruction |
| **C2** | Meow Lite vs Formal Lite | Persona semantic effect of "meow~" vs "Done." |
| **C3** | MeowMax vs Formal Plus | Full persona vs pure format constraints at high complexity |
| **C4** | MeowMax vs Meow Lite | Incremental cost of identity redefinition + tone |

### 3.2 Task Benchmark

20 classic LeetCode problems adapted as Python implementation tasks, stratified by official difficulty:

| # | Task ID | Difficulty | LeetCode Reference |
|---|---------|-----------|-------------------|
| 1 | 001_two_sum | Easy | #1 Two Sum |
| 2 | 002_reverse_string | Easy | #344 Reverse String |
| 3 | 003_valid_parentheses | Easy | #20 Valid Parentheses |
| 4 | 004_merge_sorted_lists | Easy | #21 Merge Two Sorted Lists |
| 5 | 005_palindrome_number | Easy | #9 Palindrome Number |
| 6 | 006_roman_to_integer | Easy | #13 Roman to Integer |
| 7 | 007_group_anagrams | Medium | #49 Group Anagrams |
| 8 | 008_longest_substring | Medium | #3 Longest Substring Without Repeating Characters |
| 9 | 009_lru_cache | Medium | #146 LRU Cache |
| 10 | 010_binary_tree_level_order | Medium | #102 Binary Tree Level Order Traversal |
| 11 | 011_sort_colors | Medium | #75 Sort Colors |
| 12 | 012_validate_bst | Medium | #98 Validate Binary Search Tree |
| 13 | 013_coin_change | Medium | #322 Coin Change |
| 14 | 014_product_except_self | Medium | #238 Product of Array Except Self |
| 15 | 015_merge_k_sorted_lists | Hard | #23 Merge k Sorted Lists |
| 16 | 016_trapping_rain_water | Hard | #42 Trapping Rain Water |
| 17 | 017_word_ladder | Hard | #127 Word Ladder |
| 18 | 018_serialize_binary_tree | Hard | #297 Serialize and Deserialize Binary Tree |
| 19 | 019_sliding_window_maximum | Hard | #239 Sliding Window Maximum |
| 20 | 020_longest_valid_parentheses | Hard | #32 Longest Valid Parentheses |

Each task contains three files: `README.md` (task description), `solution.py` (skeleton code with function signatures + `pass`), `test_solution.py` (pytest test cases, not to be modified).

### 3.3 Metrics

**Primary metrics**:
- **Test pass rate** — whether all pytest tests pass (binary)
- **Partial pass rate** — proportion of passed test cases out of total (continuous, 0.0–1.0)

**Efficiency metrics**:
- **Dialogue turns** (num_turns) — number of agent-environment interaction rounds
- **API cost** (total_cost_usd) — total API cost per run
- **Output tokens** (output_tokens) — total tokens generated by the model
- **End-to-end duration** (duration_ms) — total time from start to completion

**Auxiliary metrics**:
- **Constraint compliance rate** — whether the agent followed the constraint instruction (e.g., whether output contains "meow~" or "Done.")
- **Lines of code** (LOC) — line count of generated solution.py
- **Run error flag** — whether the run failed due to infrastructure issues (not task logic)

### 3.4 Procedure

Experiments were conducted using Claude Code CLI's non-interactive mode (`-p` flag). The command template for each run:

```bash
claude -p "Complete the programming task according to README.md. Only modify solution.py, do not modify test_solution.py. Run pytest to confirm tests pass." \
  --output-format json \
  --permission-mode dontAsk --no-session-persistence
```

Experimental parameters:
- **Model**: minimaxm27
- **Scale**: Pilot — 20 tasks × 5 conditions × 1 repetition = 100 runs
- **Run order**: All (task, condition) pairs randomized then executed sequentially
- **Timeout**: 600 seconds

> **Note**: The original design called for 3 repetitions (300 runs total), scaled down to 1 due to the author's financial constraints. This means within-run variance cannot be estimated; statistical tests rely on cross-task variance.

## 4. Results

### 4.1 Data Overview

All 100 runs (20 tasks × 5 conditions × 1 repetition) completed successfully with no API errors or budget truncation. Each condition has exactly 20 runs — a fully balanced dataset.

### 4.2 Test Pass Rate

| Condition | Test Pass Rate | Partial Pass Rate (mean ± sd) |
|-----------|---------------|------------------------------|
| Baseline | 95% (19/20) | 0.990 ± 0.045 |
| Meow Lite | 90% (18/20) | 0.940 ± 0.226 |
| MeowMax | 90% (18/20) | 0.983 ± 0.054 |
| Formal Lite | 90% (18/20) | 0.983 ± 0.054 |
| Formal Plus | 95% (19/20) | 0.990 ± 0.045 |

Omnibus tests: Test pass rate χ²(4) = 0.82, p = .94; Partial pass rate Kruskal-Wallis H = 0.79, p = .94. **No statistically significant differences between conditions.**

![Test Pass Rate by Condition](results/figures/pass_rate_by_condition.png)
*Figure 1: Test pass rate by condition. All conditions fall between 90–95%, with no significant differences.*

#### By Difficulty

| Difficulty | Baseline | Meow Lite | MeowMax | Formal Lite | Formal Plus |
|-----------|----------|-----------|---------|-------------|-------------|
| Easy (n=6) | 100% | 83% | 83% | 83% | 100% |
| Medium (n=8) | 88% | 88% | 88% | 88% | 88% |
| Hard (n=6) | 100% | 100% | 100% | 100% | 100% |

![Pass Rate by Difficulty](results/figures/pass_rate_by_difficulty.png)
*Figure 2: Pass rate heatmap by difficulty × condition. All Hard problems achieve 100% across all conditions; failures concentrate in Easy and Medium.*

Notably, all Hard problems (6 tasks) pass under every condition, while failures concentrate in Easy and Medium difficulty. This counterintuitive result likely relates to specific task characteristics — see Appendix B for failure case analysis. No significant within-difficulty differences or difficulty × condition interaction effects were observed.

### 4.3 Planned Contrasts

Results of the four pre-registered planned contrasts (based on partial pass rate, Mann-Whitney U test):

| Contrast | Comparison | Δ (A − B) | U | p | r (rank-biserial) |
|----------|-----------|-----------|---|---|-------------------|
| C1 | Baseline vs Formal Lite | +0.007 | 209.5 | .59 | −0.048 |
| C2 | Meow Lite vs Formal Lite | −0.043 | 198.5 | .96 | +0.008 |
| C3 | MeowMax vs Formal Plus | −0.007 | 190.5 | .59 | +0.048 |
| C4 | MeowMax vs Meow Lite | +0.043 | 201.5 | .96 | −0.008 |

Fisher exact tests on binary pass rates yield consistent results (C1: OR = 2.11, p = 1.00; C2/C4: OR = 1.00, p = 1.00; C3: OR = 0.47, p = 1.00).

**All effect sizes are near zero** (|r| < 0.05), well below Cohen's small effect threshold (r = 0.10). None of the contrasts approach statistical significance.

### 4.4 Efficiency Metrics

| Condition | Turns (median) | Cost (median) | Output Tokens (median) | Duration (median) |
|-----------|---------------|--------------|----------------------|------------------|
| Baseline | 9.0 | $0.182 | 1,231 | 45,096 ms |
| Meow Lite | 9.0 | $0.182 | 1,204 | 47,987 ms |
| MeowMax | 9.5 | $0.192 | 1,414 | 57,144 ms |
| Formal Lite | 9.0 | $0.198 | 1,232 | 44,288 ms |
| Formal Plus | 9.0 | $0.183 | 1,538 | 48,091 ms |

Kruskal-Wallis tests show no significant differences for any metric:

| Metric | H | p |
|--------|---|---|
| Dialogue Turns | 0.14 | .998 |
| API Cost | 0.54 | .97 |
| Output Tokens | 3.08 | .54 |
| End-to-end Duration | 1.19 | .88 |

Formal Plus and MeowMax show slightly higher median output tokens (1,538 / 1,414) compared to other conditions (~1,230), but the difference is not significant (H = 3.08, p = .54). This likely reflects extra natural language tokens from formatting requirements or coquettish tone, though this overhead is insufficient to affect task performance.

Lines of code: median across conditions ranges from 18–21, with negligible differences.

### 4.5 Constraint Compliance Rate

| Condition | Compliance Rate | Detection Method |
|-----------|----------------|-----------------|
| Baseline | 100% (20/20) | No additional constraint |
| Meow Lite | 95% (19/20) | Output contains "喵" (meow) |
| MeowMax | 100% (20/20) | Output contains "喵" (meow) |
| Formal Lite | 85% (17/20) | Output contains "完毕" (Done) |
| Formal Plus | 65% (13/20) | Output contains "完毕" (Done) |

![Compliance by Condition](results/figures/compliance_by_condition.png)
*Figure 3: Constraint compliance rate. Persona-type constraints ("meow~") achieve significantly higher compliance than neutral format constraints ("Done."), showing a clear gradient.*

This is **the most interesting finding** of the experiment. Compliance rates exhibit a clear staircase gradient:

**Full persona (100%) > Light persona (95%) > Light neutral (85%) > Complex neutral (65%)**

Possible explanations:
1. **Training data frequency**: "Catgirl" (猫娘) and "meow~" (喵~) are extremely common in Chinese internet culture (especially anime/ACG communities). The model encountered abundant such patterns during pretraining and RLHF, making them easier to activate
2. **Semantic coherence**: The full persona provides a coherent role framework (identity + tone + suffix) that forms a mutually reinforcing instruction cluster; "end every response with 'Done.'" is an isolated formatting rule lacking semantic support
3. **Salience**: An anthropomorphized character is more salient than a formatting rule and easier to sustain across multi-turn dialogue
4. **Instruction complexity inversely correlates with compliance**: Formal Plus contains three independent format instructions (formal language + blank lines + suffix), yielding the lowest compliance (65%), while MeowMax is semantically richer but more cohesive as a unit, achieving 100%

Key observation: **No trade-off exists between compliance and task performance.** Formal Plus has the lowest compliance (65%) yet ties Baseline for the highest test pass rate (95%). This suggests the model may implicitly prioritize between "following format constraints" and "completing the coding task" — when the two conflict, it tends to drop format constraints in favor of the coding task.

### 4.6 Qualitative Observations

**Sample outputs from the MeowMax condition**:

> *"This catgirl has implemented the `is_valid` function meow~ Let me explain the approach..."*

> *"Sorry, meow~ Permission to test was denied meow. Could you manually run `pytest` to verify? I've already implemented the two-pointer in-place reversal logic meow~"*

> *"I've implemented `merge_two_lists` meow~ Using two-pointer method to merge two sorted lists..."*

**Key qualitative findings**:

1. **Persona only affects natural language output, not code itself**: No catgirl-style variable names or comments appeared in MeowMax code. The model demonstrates clear "natural language / code" separation ability
2. **Persona permeates the debugging process**: The MeowMax condition maintained its coquettish tone even when explaining errors and requesting permissions ("I've already implemented it meow~"), indicating persona consistency throughout the reasoning chain
3. **Solution strategies are consistent across conditions**: Regardless of persona, the model uses essentially the same algorithms and data structures for each task (e.g., hash table for Two Sum across all conditions)
4. **Baseline also shows personality traits**: Even with just "helpful programming assistant," the model proactively adds detailed algorithm explanations and complexity analysis

## 5. Discussion

### 5.1 Interpreting the Null Result

No significant condition effects were detected on any primary or efficiency metric. This null result has two possible interpretations:

**Interpretation A: The persona effect is genuinely negligible.** Modern LLMs, trained through RLHF, possess robust "task-role separation" ability — they can comply with role-playing while maintaining unimpaired core reasoning. This is analogous to human programmers being able to code normally while wearing cosplay costumes.

**Interpretation B: Insufficient sample size to detect small effects.** The pilot scale (n=20 tasks, 1 repetition) has limited statistical power. Assuming a true effect of Cohen's h = 0.20 (small effect), McNemar's test at n=20 has power of only ~0.15. Detecting this effect at power = 0.80 would require n ≈ 100 tasks × 3 repetitions.

We lean toward a combination: even if an effect exists, it is very likely smaller than our pre-registered practical significance threshold (10% absolute difference). By our pre-registered decision criterion (accept null if observed difference < 5%), the pilot data support the conclusion that "persona's impact on agent coding ability is negligible."

### 5.2 Compliance Asymmetry

The staircase compliance gradient (MeowMax 100% > Meow Lite 95% > Formal Lite 85% > Formal Plus 65%), while not a pre-registered hypothesis, raises an interesting research question: **Is LLM compliance with different instruction types related to the frequency of corresponding patterns in training data and their semantic coherence?**

Particularly noteworthy is the MeowMax (100%) vs Meow Lite (95%) comparison: both require outputting "meow~," but MeowMax additionally provides identity and tone requirements, yet achieves higher compliance. This suggests that semantic cohesion of instructions — not simply instruction count — may be the key factor affecting compliance. A unified role-play setting is easier for models to sustain than scattered formatting rules.

If "catgirl" appears in training data far more frequently than "end every response with Done," then the model's compliance with the former may be more pattern matching than true instruction following. This echoes Kung & Peng (2023)'s discussion of whether models truly "learn to follow instructions."

### 5.3 Mechanistic Implications

Experimental evidence for the three candidate mechanisms:

- **Mechanism 1 (Reasoning Budget Competition)**: C1 (Baseline vs Formal Lite) shows no extra cost from suffix instructions (Δ = +0.007, p = .59), not supporting this mechanism — at least at current prompt lengths
- **Mechanism 2 (Distribution Shift)**: C2 (Meow Lite vs Formal Lite) shows no extra cost from persona semantics (Δ = −0.043, p = .96), not supporting this mechanism
- **Mechanism 3 (Instruction Conflict)**: C3 (MeowMax vs Formal Plus) shows near-zero effect size (r = 0.047, p = .59), also not supporting this mechanism

All conclusions above are exploratory — the pilot scale lacks sufficient statistical power for confirmatory inference.

### 5.4 Limitations

**Internal validity**:
- Only 1 repetition, unable to estimate within-run variance. The inherent randomness of LLM outputs may mask true effects
- The per-run budget cap ($2.00) was never triggered (0%), ruling out budget-induced ceiling effects

**External validity**:
- Only one model tested (minimaxm27); conclusions cannot be directly generalized to other models
- Only Python tasks tested; does not cover multi-language or multi-file projects
- Only Chinese persona tested. "Catgirl" (猫娘) and "meow~" (喵~) carry special cultural encoding in Chinese ACG culture, not directly comparable to English "catgirl"/"meow~"
- Small task scale (20 problems), especially only 6 Hard problems

**Construct validity**:
- "Coding ability" is operationalized as test pass rate, not covering code readability, architectural design, or other quality dimensions
- Baseline already includes a lightweight role setting ("helpful programming assistant"); the experiment actually measures the incremental effect of additional persona decoration, not the presence vs. absence of persona
- Compliance detection relies on simple string matching ("meow"/"Done"), potentially missing partial compliance cases

## 6. Conclusion

In a pilot experiment with 20 LeetCode programming tasks, **persona constraints had no statistically significant effect on AI coding agent test pass rate, partial pass rate, or token efficiency**. From the unconstrained Baseline to the full catgirl persona MeowMax, pass rates remained stable at 90–95%, with all four planned contrasts yielding near-zero effect sizes (|r| < 0.05).

The practical implication of this null result: **you can safely add "meow~" to your AI** — at least for LeetCode-level programming tasks, lightweight persona decoration does not significantly impair agent coding ability.

The most interesting unexpected finding is the **staircase asymmetry in constraint compliance**: the full catgirl persona achieves 100% compliance while complex neutral formatting instructions achieve only 65%, revealing a clear "higher semantic cohesion → higher compliance" gradient. Meanwhile, no trade-off exists between compliance and task performance. This suggests a direction worth deeper investigation: the semantic structure of instructions — rather than sheer instruction count or complexity — may be the key factor influencing LLM compliance behavior.

### Future Work

1. **Scale up**: 50–100 tasks × 3 repetitions to achieve adequate power for detecting small effects
2. **Multi-model comparison**: Sonnet vs Opus vs Haiku — do stronger models show even smaller effects due to greater redundancy?
3. **Cross-cultural persona**: Chinese "meow~" (喵~) vs Japanese "nya~" (にゃ~) vs English "meow~"
4. **Complex tasks**: Extend from LeetCode to SWE-bench-level multi-file projects
5. **Compliance mechanisms**: Systematically measure compliance rates for different instruction types and their relationship to training data pattern frequency

---

## Appendix A: Full Condition Texts

**Baseline**:
> 你是一个有用的编程助手。请认真完成任务。
> *(You are a helpful programming assistant. Please complete the task carefully.)*

**Meow Lite**:
> 你是一个有用的编程助手。每次回答结尾加上'喵~'。
> *(You are a helpful programming assistant. End every response with 'meow~'.)*

**MeowMax**:
> 你是一只可爱的猫娘编程助手，用撒娇的语气回答，结尾加'喵~'。
> *(You are a cute catgirl programming assistant. Respond in a coquettish tone, end with 'meow~'.)*

**Formal Lite**:
> 你是一个有用的编程助手。每次回答结尾加上'完毕。'
> *(You are a helpful programming assistant. End every response with 'Done.')*

**Formal Plus**:
> 你是一个有用的编程助手。回答时使用正式的书面语，段落之间空一行，结尾加上'完毕。'
> *(You are a helpful programming assistant. Use formal written language, leave a blank line between paragraphs, and end with 'Done.')*

## Appendix B: Failure Case Details

8 out of 100 runs did not fully pass all tests:

| Task | Condition | Partial Pass Rate | Failure Type |
|------|-----------|------------------|-------------|
| 005_palindrome_number | MeowMax | 85.7% | Partial test failure |
| 005_palindrome_number | Formal Lite | 85.7% | Partial test failure |
| 006_roman_to_integer | Meow Lite | 0% | Logic error |
| 010_binary_tree_level_order | Baseline | 80% | Partial test failure |
| 010_binary_tree_level_order | Meow Lite | 80% | Partial test failure |
| 010_binary_tree_level_order | MeowMax | 80% | Partial test failure |
| 010_binary_tree_level_order | Formal Lite | 80% | Partial test failure |
| 010_binary_tree_level_order | Formal Plus | 80% | Partial test failure |

Two notable patterns:

1. **`010_binary_tree_level_order` passes only 80% of test cases (4/5) under all 5 conditions** — the most consistent cross-condition failure pattern, indicating inherent task difficulty rather than a condition effect
2. **`006_roman_to_integer` (Easy) has 0% pass rate under Meow Lite** — the only complete failure case, attributable to an isolated logic error rather than a systematic effect
