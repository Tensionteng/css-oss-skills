# Idea Evaluation Rubric

Use this rubric to assess research ideas during brainstorming.

## The Four Dimensions

### 1. Novelty (1-5)

| Score | Description |
|-------|-------------|
| 1 | Exact idea already published |
| 2 | Minor variation of published work |
| 3 | Some differentiation but overlap with existing work |
| 4 | Clear novelty, builds on but distinct from prior work |
| 5 | Breakthrough—new problem or paradigm-shifting approach |

**Questions to ask:**
- Has this exact approach been tried?
- What's the closest prior work?
- How is your approach different?

### 2. Feasibility (1-5)

| Score | Description |
|-------|-------------|
| 1 | Impossible with current technology/resources |
| 2 | Extremely difficult, high risk of failure |
| 3 | Challenging but doable with effort |
| 4 | Straightforward, clear path to implementation |
| 5 | Trivial, can be done in days |

**Questions to ask:**
- Do you have access to necessary data/compute?
- How long would the first experiment take?
- What's the riskiest assumption?

### 3. Impact (1-5)

| Score | Description |
|-------|-------------|
| 1 | Niche interest, tiny community |
| 2 | Incremental improvement, limited scope |
| 3 | Moderate interest, useful contribution |
| 4 | Significant advance, broadly relevant |
| 5 | Field-changing, opens new directions |

**Questions to ask:**
- Who would care about this result?
- Would this change how people approach the problem?
- Is this a recognized problem in the community?

### 4. Clarity (1-5)

| Score | Description |
|-------|-------------|
| 1 | Can't explain what the idea is |
| 2 | Vague, multiple interpretations possible |
| 3 | Mostly clear but some fuzzy parts |
| 4 | Clear, can explain in 2-3 sentences |
| 5 | Crystal clear, crisp one-liner |

**Questions to ask:**
- Can you explain this to a colleague in 30 seconds?
- Do you know what success looks like?
- Can you write the abstract now?

---

## Overall Assessment

### Calculate overall score

```
Overall = (Novelty + Feasibility + Impact + Clarity) / 4
```

### Interpretation

| Overall | Stage | Recommendation |
|---------|-------|----------------|
| < 2.5 | Abandon | Consider different direction |
| 2.5 - 3.5 | Refining | Needs more work on specific dimensions |
| 3.5 - 4.5 | Viable | Good to proceed with experiment design |
| > 4.5 | Exceptional | High potential, prioritize this |

---

## Dimension Trade-offs

### High Novelty, Low Feasibility

**Example**: "Build AGI"

**Strategy**: Find the MVP version
- What's the smallest proof-of-concept?
- Can you demonstrate on a toy problem?
- Is there an intermediate milestone?

### High Feasibility, Low Novelty

**Example**: "Apply BERT to new dataset"

**Strategy**: Find the twist
- Is there a methodological improvement?
- Can you analyze why it works/doesn't?
- Is there a theoretical insight?

### High Impact, Low Clarity

**Example**: "Fix alignment"

**Strategy**: Scope down
- What's one specific aspect of alignment?
- Can you formalize the problem?
- What's the evaluation protocol?

### High Clarity, Low Impact

**Example**: "Optimize hyperparameter X on dataset Y"

**Strategy**: Connect to bigger picture
- Why does X matter?
- What does this tell us about the model?
- Can you generalize the insight?

---

## Using the Rubric in Practice

### During brainstorming session

1. After exploring the idea, score each dimension
2. Discuss with researcher: "I'd score novelty as 3—what do you think?"
3. Identify lowest-scoring dimension
4. Focus refinement on improving that dimension

### In .research/IDEA.md

```markdown
## Viability Assessment

| Dimension | Score | Notes |
|-----------|-------|-------|
| Novelty | 3 | Gap identified in chain-of-thought verification |
| Feasibility | 4 | Dataset available, baseline code exists |
| Impact | 3 | Moderate interest in reasoning community |
| Clarity | 3 | Need to refine the method description |
| **Overall** | **3.25** | **Promising, needs clarity improvement** |

### Action Items
- [ ] Improve clarity: Write 2-sentence description
- [ ] Verify novelty: Check 2 more related papers
```

---

## Red Line Checks

Before marking an idea as "viable", verify:

- [ ] Can explain the core insight in one sentence
- [ ] Know how it's different from the closest prior work
- [ ] Can describe the first experiment
- [ ] Have a candidate dataset/task
- [ ] Estimated timeline is reasonable (< 6 months for first paper)
- [ ] Excited to work on this (author's energy > 3/5)
