# Pilot Experiment Design

## Principles

### 1. Start with the Core Claim

Your pilot should answer: **"Does our core idea work at all?"**

Not:
- ❌ "Is this SOTA?" (too ambitious for pilot)
- ❌ "Does it work on all datasets?" (too broad)

But:
- ✅ "Does verification reduce arithmetic errors?"
- ✅ "Can the model learn the new objective?"

### 2. Minimize Variables

**Fixed for pilot**:
- One dataset (smallest viable)
- One model size (smallest that can show the effect)
- Minimal hyperparameter tuning

**Only variable**: Your method vs baseline

### 3. Clear Success Criteria

Before running, define:
```
"Pilot succeeds if:
- Our method achieves >80% accuracy on 100-sample subset
- Improvement over baseline is >5 points
- Training converges within 1 hour"
```

## Pilot Size Guidelines

| Resource | Pilot Size | Example |
|----------|-----------|---------|
| **Data** | 100-1000 samples | Subset of full dataset |
| **Model** | Small/medium | GPT-2 small, ResNet-18 |
| **Time** | 1-4 hours | Quick training run |
| **Compute** | 1 GPU | Single V100/A100 |

## Common Pilot Patterns

### Pattern: Toy Problem

**When**: Method is complex, need to verify it works at all

**Setup**:
- Create synthetic/toy dataset where solution is known
- Verify method can solve it
- Scale to real data only after toy works

**Example**:
```
Toy: Sorting 10 numbers with custom attention
Real: Sorting variable-length sequences
```

### Pattern: Subset Validation

**When**: Full dataset is large, but subset is representative

**Setup**:
- Random 1% sample of training data
- Evaluate on full validation (if fast) or subset
- Check if trend holds

**Example**:
```
Full: GSM8K (8K problems)
Pilot: GSM8K-100 (random 100 problems)
```

### Pattern: Downstream Proxy

**When**: Final evaluation is expensive, but proxy exists

**Setup**:
- Find cheap metric that correlates with final goal
- Optimize for proxy in pilot
- Verify correlation on small sample

**Example**:
```
Final: Human evaluation of generation quality
Pilot: BLEU/ROUGE scores (fast, automatic)
```

### Pattern: Ablation-First

**When**: Not sure which components matter

**Setup**:
- Start with full method on tiny scale
- Remove components one by one
- Identify minimum viable method

**Example**:
```
Pilot 1: Full method (verification + reranking + ensemble)
Pilot 2: Verification only
Pilot 3: Reranking only
→ Learn: Verification is the key component
```

## Decision Matrix

After pilot, decide:

| Result | Decision | Action |
|--------|----------|--------|
| **Clear success** | Scale up | Design larger experiment |
| **Partial success** | Adjust | Identify issue, fix, re-pilot |
| **Unexpected finding** | Explore | Follow the new lead |
| **Clear failure** | Pivot/Abandon | Back to brainstorming |

## Pilot Checklist

Before starting:
- [ ] Core claim is clearly stated
- [ ] Success criteria are defined
- [ ] Dataset is prepared
- [ ] Baseline code runs
- [ ] Expected runtime is acceptable
- [ ] Evaluation script ready

After pilot:
- [ ] Results logged
- [ ] Comparison with baseline done
- [ ] Analysis written
- [ ] Decision made
- [ ] Next step planned

## Common Mistakes

### ❌ Pilot Too Big
**Mistake**: Trying to match SOTA on first run
**Fix**: Start with proof-of-concept, not SOTA comparison

### ❌ No Baseline
**Mistake**: Only running your method
**Fix**: Always compare to something (even simple baseline)

### ❌ Moving Goalposts
**Mistake**: Changing success criteria after seeing results
**Fix**: Define criteria before running

### ❌ Ignoring Negative Results
**Mistake**: Only reporting what worked
**Fix**: Document failures—they're informative

### ❌ Perfectionism
**Mistake**: Tweaking for weeks before first run
**Fix**: Run ugly pilot quickly, learn, iterate

## Example Pilot Designs

### Example 1: Verification Method

```markdown
## Pilot 1: Verification Reduces Errors

### Core Claim
Adding a verification step reduces arithmetic errors in math reasoning.

### Setup
- Dataset: GSM8K-100 (random 100 problems)
- Model: GPT-2 small (124M)
- Baseline: Standard chain-of-thought
- Our method: CoT + verification step

### Success Criteria
- Our method > baseline by >10 points
- Verification catches >50% of errors
- Runtime < 2x baseline

### Expected Time
- Training: 30 min on 1x A100
- Evaluation: 5 min

### Analysis Plan
- Error analysis: What does verification catch?
- Failure modes: What does it miss?
- Cost-benefit: Accuracy vs runtime tradeoff
```

### Example 2: New Architecture

```markdown
## Pilot 1: Architecture Works at All

### Core Claim
New attention variant can be trained and converges.

### Setup
- Dataset: Toy copy task (sequence length 10)
- Model: 2-layer transformer with new attention
- Baseline: Standard attention (same size)

### Success Criteria
- Training loss decreases
- Reaches near-zero loss on toy task
- No NaN/instability

### Expected Time
- Training: 10 min on CPU

### Analysis Plan
- Loss curves: Does it converge?
- Attention patterns: Does it learn meaningful weights?
- Memory/time: Overhead vs standard attention?
```
