# Result Analysis Guide

## Questions to Answer

### 1. Did It Work?

**Quantitative**:
- Did we meet success criteria?
- How much better/worse than baseline?
- Is improvement statistically significant?

**Qualitative**:
- Do results make sense?
- Any surprising patterns?
- Consistent across different settings?

### 2. Why Did It Work (or Not)?

**If successful**:
- What aspect of method is responsible?
- Which component matters most? (ablations)
- When does it work best?

**If failed**:
- What went wrong?
- Is it fixable?
- Should we pivot?

### 3. What's Next?

- Scale up?
- Fix issues and retry?
- Explore unexpected findings?
- Abandon and pivot?

## Analysis Framework

### Quantitative Analysis

#### Absolute Performance
```
Our method: 85.2%
Baseline: 78.5%
Improvement: +6.7 points (+8.5% relative)
```

#### Statistical Significance
```
Run 5 seeds, report mean ± std:
Ours: 85.2 ± 1.3
Baseline: 78.5 ± 2.1
→ Significant improvement (p < 0.05)
```

#### Ablation Analysis
```
Full method: 85.2%
- w/o Component A: 82.1% (-3.1)
- w/o Component B: 79.8% (-5.4)
→ Component B is more important
```

### Qualitative Analysis

#### Error Analysis

Categorize failures:
```
Total errors: 100
- Category 1 (e.g., arithmetic): 40
- Category 2 (e.g., reasoning): 35
- Category 3 (e.g., knowledge): 25

Our method fixes: 30/40 Category 1 errors
But introduces: 5 new Category 2 errors
```

#### Case Studies

Show concrete examples:
```
Example 1: Where our method succeeds
[Input]
[Baseline output - wrong]
[Our output - correct]
[Analysis: why did we get it right?]

Example 2: Where our method fails
[Input]
[Correct answer]
[Our output - wrong]
[Analysis: why did we get it wrong?]
```

## Documenting Results

### In .research/EXPERIMENT.md

```markdown
## Pilot X Results (Date)

### Configuration
- Dataset: 
- Model: 
- Hyperparameters: 

### Main Results
| Metric | Baseline | Ours | Δ |
|--------|----------|------|---|
| Accuracy | 78.5 | 85.2 | +6.7 |

### Ablations
| Variant | Accuracy | Δ |
|---------|----------|---|
| Full | 85.2 | - |
| w/o A | 82.1 | -3.1 |
| w/o B | 79.8 | -5.4 |

### Analysis
**What worked**:
- 

**What didn't**:
- 

**Surprises**:
- 

**Explanation**:
[Why these results make sense]

### Decision
[Continue / Adjust / Pivot / Abandon]

### Next Steps
- 
```

## Common Analysis Patterns

### Pattern: Better on Some, Worse on Others

**Observation**:
```
Dataset A: 85% (+5 over baseline) ✓
Dataset B: 72% (-3 vs baseline) ✗
```

**Analysis**:
- What's different about Dataset B?
- Does our method make assumptions that B violates?
- Can we adapt method for B?

**Decision options**:
- Focus on A (narrow scope)
- Understand and fix B issue
- Report both honestly (not all methods work everywhere)

### Pattern: High Variance

**Observation**:
```
Run 1: 90%
Run 2: 75%
Run 3: 88%
→ High variance, unreliable
```

**Possible causes**:
- Random seed sensitivity
- Small dataset size
- Training instability
- Bug in code

**Actions**:
- More seeds
- Debug instability
- Larger dataset
- Check for bugs

### Pattern: Training Doesn't Converge

**Observation**:
Loss oscillates or increases

**Possible causes**:
- Learning rate too high
- Bug in loss function
- Gradient explosion
- Bad initialization

**Actions**:
- Lower learning rate
- Add gradient clipping
- Check loss implementation
- Try different init

### Pattern: Overfitting

**Observation**:
Train accuracy: 95%
Val accuracy: 70%

**Actions**:
- Add regularization
- More data
- Simpler model
- Early stopping
- Check for data leakage

## Visualization Best Practices

### Learning Curves
- Plot train and val loss/accuracy
- Show multiple seeds (mean ± std)
- Mark important events (lr decay, etc.)

### Comparison Plots
- Bar charts for final performance
- Error bars for variance
- Statistical significance markers (*)

### Ablation Studies
- Grouped bar chart
- Include full method as reference
- Show both absolute and relative drop

### Error Analysis
- Pie chart of error categories
- Before/after comparison
- Per-category improvement

## When to Trust Results

### ✅ Good Signs
- Consistent across multiple runs
- Reproducible (colleague can replicate)
- Makes sense theoretically
- Matches intuition/prior work

### ⚠️ Warning Signs
- Too good to be true (beat SOTA by 20%)
- Only works on one specific setting
- High variance between runs
- Can't explain why it works
- Results change with random seed

### 🛑 Red Flags
- Only evaluated on training set
- Test data leaked into training
- Cherry-picked best result
- Can't reproduce own results
- Violates basic theoretical constraints

## Communication

### To Advisor/Team
```
"Pilot 1 is complete. Key findings:
- Achieved 85% vs 78% baseline (+7 points)
- Main driver is Component B (ablation shows -5 without it)
- One surprise: performs worse on small data
- Decision: Proceed to Pilot 2 with larger dataset
```

### To Yourself (Notes)
```
"Tried lr=1e-3, didn't converge. lr=1e-4 works.
Batch size 32 OOM, using 16.
Found bug in data loader (fixed, rerunning).
```

### For Paper (Later)
```
"Our method achieves 85.2% accuracy, outperforming 
 the previous SOTA of 78.5% [citation]. Ablation 
 studies show that Component B contributes most to 
 performance (5.4 point drop when removed)."
```
