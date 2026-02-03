# Baseline Selection Guide

## What Makes a Good Baseline

### Criteria

| Criterion | Why It Matters | How to Check |
|-----------|---------------|--------------|
| **Relevance** | Solves same problem | Compare problem definitions |
| **Recency** | Represents current SOTA | Check publication year |
| **Recognition** | Community accepts it | Check citations, venue |
| **Reproducibility** | You can actually run it | Check code availability |
| **Comparability** | Same setting/metrics | Check experimental setup |

### Red Flags

- ❌ **Too old** (>3 years in fast-moving field)
- ❌ **Wrong setting** (different data split, different metric)
- ❌ **Not reproducible** (no code, vague description)
- ❌ **Unfair comparison** (your method uses extra data/training)
- ❌ **Straw man** (choosing weak baseline to look good)

## Types of Baselines

### 1. Standard/De Facto Baseline

**What**: Method everyone compares against

**Example**: 
- Transformers for NLP
- ResNet for vision
- Standard CoT for reasoning

**When to use**: Always include as reference point

### 2. SOTA Method

**What**: Current best reported result

**Example**:
- Best paper on leaderboard
- Recent high-citation method

**When to use**: Show you improve over best known method

### 3. Ablated Versions

**What**: Your method minus components

**Example**:
- Full method → remove module A → remove module B

**When to use**: Show each component contributes

### 4. Simpler Alternatives

**What**: Easier methods that might work

**Example**:
- Heuristic/rule-based
- Simple ML (logistic regression)
- Smaller model

**When to use**: Show complexity is justified

## Finding the Right Baseline

### Step 1: Check Recent Papers

Look at papers from last 2 years on same task:
- What do they compare against?
- What's their main baseline?
- What SOTA do they claim to beat?

### Step 2: Check Leaderboards

If available:
- Papers With Code
- Official benchmarks (GLUE, SuperGLUE, etc.)
- Competition results (Kaggle, etc.)

### Step 3: Verify with Researcher

Questions to ask:
- "Who is the established leader in this area?"
- "What method would reviewers expect us to compare to?"
- "Is there a method you specifically want to beat?"

## Documenting Baselines

In `.research/SOTA.md`:

```markdown
## Selected Baselines

### Primary: [Paper Name] ([arXiv ID])
- **Why selected**: Current SOTA on our target dataset
- **Method**: [Brief description]
- **Reported results**: 
  - Dataset X: 92.3%
  - Dataset Y: 85.1%
- **Our reproduction**: [TBD]
- **Code**: [link if available]

### Secondary: [Paper Name]
- **Why selected**: Classic/standard method
- **Method**: [Brief description]
- ...

### Ablations (Our Method)
- Full method
- Without component A
- Without component B
```

## Fair Comparison Checklist

- [ ] Same train/val/test split
- [ ] Same evaluation metric
- [ ] Same data preprocessing
- [ ] Comparable model size (if relevant)
- [ ] Comparable compute budget
- [ ] Same random seeds (or averaged over multiple)
- [ ] Reported confidence intervals or variance

## Common Pitfalls

### Unfair Advantage

❌ **Your method**: Trained on extra data
✅ **Fix**: Train baseline on same data, or remove extra data

❌ **Your method**: Uses ensemble, baseline is single model
✅ **Fix**: Compare ensemble vs ensemble, or single vs single

❌ **Your method**: Hyperparameter tuned extensively
✅ **Fix**: Give baseline same tuning budget

### Setting Mismatch

❌ **Baseline**: Results on different dataset split
✅ **Fix**: Re-run baseline on your split, or find compatible results

❌ **Baseline**: Different metric (e.g., F1 vs accuracy)
✅ **Fix**: Compute same metric for both

### Reproducibility Issues

❌ **Baseline**: No code available, paper vague
✅ **Fix**: Email authors, try to reproduce from paper, or choose different baseline

❌ **Baseline**: Code available but doesn't run
✅ **Fix**: Document efforts, consider alternative baseline

## Baseline Analysis Template

After analyzing baseline paper:

```markdown
## Baseline: [Paper Title]

### Metadata
- arXiv ID: 
- Year: 
- Venue: 
- Citations: 

### Method Summary
[1-2 paragraphs describing approach]

### Key Results (from paper)
| Dataset | Metric | Value |
|---------|--------|-------|
| | | |

### Experimental Setup
- Model: 
- Training: 
- Data: 

### Strengths
- 

### Limitations (acknowledged in paper)
- 

### How We Differ
[Our approach vs theirs]

### Can We Use This?
- [ ] Code available
- [ ] Can reproduce
- [ ] Comparable setting
- [ ] Fair comparison possible
```
