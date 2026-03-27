---
name: research-execution
description: Execute research experiments through progressive pilot studies. Design experiments, run pilots at increasing scales, and analyze results. Maintains .research/EXPERIMENT.md.
metadata:
  author: tengshiyuan
  tags: [Research, Experiments, Pilot Studies, Baseline Analysis, Evaluation]
  dependencies: [pymupdf, semanticscholar]
---

# Research Execution

Guide researchers through **progressive pilot studies** to validate research ideas. This is an **iterative, conversational** skill—experiments often reveal new insights that require adjusting the approach.

## Core Philosophy: Progressive Scaling

Research experiments should start small and scale up based on results:

```
Pilot (small data/small model)
    ↓
Result good? → Scale up (medium)
    ↓
Result good? → Full scale (SOTA comparison)
    ↓
Enough evidence? → Write paper
    ↓
New insight? → Update IDEA, iterate
```

**At each stage**, ask: "Does this support our claim? Should we continue, adjust, or pivot?"

---

## Prerequisites

Before using this skill, ensure:
1. `.research/IDEA.md` exists with **viable angle** (from brainstorming)
2. **Codebase ready** (`AGENTS.md` from `/init` if using existing code)
3. **`pdf-reader` skill installed** (for analyzing baseline papers)

---

## Workflow Overview

### Step 1: Setup Check
Read `.research/IDEA.md` and check if we're ready to start experiments.

### Step 2: SOTA & Baseline
Identify the SOTA method to compare against. Requires **pdf-reader** skill.

### Step 3: Pilot Design  
Design smallest experiment that can validate the core claim.

### Step 4: Execute & Learn
Run pilot, analyze results, decide next step.

### Step 5: Scale or Pivot
Based on pilot results: scale up, adjust design, or go back to brainstorming.

---

## Detailed Workflows

### Workflow 1: SOTA & Baseline Analysis

**Goal**: Understand what we're comparing against.

**Option A: Researcher provides baseline**
```
Researcher: "Use arXiv:2405.12345 as baseline"

AI:
1. Check if pdf-reader skill available
2. Convert paper to images:
   uv run python ../pdf-reader/scripts/convert.py \
       --arxiv 2405.12345 \
       --output .research/baselines/paper-1/

3. Read key pages with ReadMediaFile:
   - page_001.png: Title, abstract
   - Find method section (scan pages)
   - Find experiments section (read results table)

4. Extract to .research/SOTA.md:
   - Method: [summary]
   - Metrics: [what they measure]
   - SOTA numbers: [dataset: value]
   - Key innovation: [what's new]

5. Confirm with researcher:
   "This paper achieves X on Y dataset using Z method. 
    Is this the right baseline to compare against?"
```

**Option B: AI searches for baseline**
```
AI:
1. Search recent high-citation papers (semanticscholar)
2. Search for surveys/overviews in the area
3. Present 2-3 candidates with:
   - Citation count (popularity)
   - Year (recency)
   - Abstract (relevance)
   - SOTA claim (from abstract/title)

4. Researcher selects one or provides alternative

5. Analyze selected paper (use pdf-reader)
```

### Workflow 2: Pilot Experiment Design

**Goal**: Design smallest experiment that validates the claim.

**Key decisions** (discuss with researcher):

| Decision | Questions |
|----------|-----------|
| **Dataset** | "What's the smallest dataset that can show our method works?" |
| **Model** | "Can we use a small model first, or do we need large?" |
| **Baselines** | "Besides SOTA, what simpler baselines should we compare?" |
| **Metrics** | "What metric best captures our improvement?" |
| **Ablations** | "What components are essential? What should we ablate?" |

**Record in .research/EXPERIMENT.md**:
```markdown
## Pilot 1 Design

### Goal
Validate that [specific claim] works on [small scale]

### Setup
- Dataset: [name] ([size] samples)
- Model: [architecture, size]
- Baselines: [list]
- Metrics: [primary, secondary]

### Expected Result
[What would convince us this is worth scaling?]

### Time Estimate
[X] hours on [GPU type]
```

### Workflow 3: Execute Pilot

**Goal**: Run the pilot and analyze results.

**Process**:
1. **Implement** (AI can help generate code)
2. **Run** (researcher executes, may take hours/days)
3. **Analyze** (when results ready)

**Analysis questions**:
- Did we meet the expected result?
- What surprised us?
- What went wrong?
- What's the explanation?

**Record in .research/EXPERIMENT.md**:
```markdown
## Pilot 1 Results (2026-01-30)

### Outcome
[Success / Partial / Failure]

### Key Numbers
- Our method: [X]%
- Baseline: [Y]%
- Improvement: [Z]%

### Observations
- [What worked]
- [What didn't]
- [Unexpected findings]

### Insights
[New understanding about the problem/method]

### Decision
- [ ] Continue to larger scale
- [ ] Adjust design and re-run
- [ ] Pivot to different angle
- [ ] Abandon this direction
```

### Workflow 4: Iterate or Scale

**Based on Pilot 1 results**:

**Path A: Success → Scale up**
- Design Pilot 2 (larger dataset/model)
- Keep what worked, add new questions
- Update .research/IDEA.md with learnings

**Path B: Partial → Adjust**
- Identify what didn't work
- Modify approach (update EXPERIMENT.md design)
- Run Pilot 1.5 (quick validation)

**Path C: Failure → Pivot/Abandon**
- Analyze why it failed
- Does it invalidate the core idea? → Back to brainstorming
- Is it a fixable issue? → Adjust and retry

**Path D: Discovery → Update IDEA**
- Found something unexpected?
- May be more interesting than original idea
- Update .research/IDEA.md with new angle
- Decide if to pursue this instead

---

## .research/EXPERIMENT.md Template（中文撰写）

```markdown
---
status: design  # design / pilot / scaling / analyzing / done
pilots_completed: 0
last_pilot: null
---

# 实验计划

## 来自 IDEA.md
[复制相关内容: 研究角度, 核心主张, 差异化]

## SOTA Baseline
[来自 SOTA 分析]

## Pilot 历史

### Pilot 1
#### 设计
[设置, 数据集, 模型, 指标]

#### 结果
[发生了什么]

#### 学到的东西
[学到了什么]

#### 决策
[继续 / 调整 / 放弃]

### Pilot 2
...

## 当前状态
- [ ] 已确定 SOTA
- [ ] 已设计 Pilot 1
- [ ] 已执行 Pilot 1
- [ ] 已做出决策

## 下一步行动
[具体下一步]
```

---

## Integration with Other Skills

### Using pdf-reader
```bash
# Convert baseline paper
uv run python .kimi/skills/pdf-reader/scripts/convert.py \
    --arxiv 2405.12345 \
    --output .research/baselines/sota-paper/

# Read with AI
ReadMediaFile(path=".research/baselines/sota-paper/page_001.png")
```

### Back to research-brainstorming
If pilot reveals need to pivot:
```
AI: "Pilot results suggest our original approach may not work because [X]. 
      Should we go back to brainstorming to explore alternatives?"

# Update .research/IDEA.md status to "revising"
# Switch to research-brainstorming skill
```

### Forward to manuscript-writing
When enough evidence collected:
```
AI: "We have completed [N] pilots with consistent results.
      Ready to move to paper writing?"

# Prepare summary for manuscript-writing
# Include: main results, key findings, limitations
```

---

## Common Patterns

### Pattern: Pilot Failed, But Fixable
```
Observation: Method works on simple cases but fails on complex ones
Analysis: Verification threshold too strict
Decision: Adjust threshold, run Pilot 1.5 (quick check)
```

### Pattern: Better Than Expected
```
Observation: Results much better than predicted
Analysis: May have discovered something more fundamental
Decision: Update IDEA.md with refined claim, design new experiments
```

### Pattern: Partial Success
```
Observation: Works on Dataset A but not Dataset B
Analysis: Method has specific conditions where it works
Decision: Narrow scope to applicable setting, or understand why B fails
```

### Pattern: Unexpected Discovery
```
Observation: Side effect more interesting than main result
Analysis: Error analysis reveals new phenomenon
Decision: Update IDEA.md to focus on new finding
```

---

## When to Stop

**Enough evidence when**:
- [ ] Core claim validated at appropriate scale
- [ ] Key ablations show what matters
- [ ] Comparison with SOTA demonstrates improvement
- [ ] Failure modes understood
- [ ] Researcher confident in results

**Not enough yet**:
- Only worked on toy dataset
- Results inconsistent across runs
- Don't understand why it works
- Key comparison missing

---

## Scripts

### find_sota.py
Find SOTA papers for a task:
```bash
uv run python scripts/find_sota.py \
    --task "math reasoning" \
    --dataset "GSM8K" \
    --output .research/sota-candidates.json
```

### exp_tracker.py
Track experiment status:
```bash
uv run python scripts/exp_tracker.py \
    --update "Pilot 1 completed" \
    --status "analyzing"
```

---

## References

- **Pilot study design**: [references/pilot-design.md](references/pilot-design.md)
- **Baseline selection**: [references/baseline-selection.md](references/baseline-selection.md)
- **Ablation strategies**: [references/ablation-design.md](references/ablation-design.md)
- **Result interpretation**: [references/result-analysis.md](references/result-analysis.md)
