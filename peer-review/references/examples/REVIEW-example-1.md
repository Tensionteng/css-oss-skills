# Review Report: Round 1

**Date**: 2026-01-31
**Reviewer**: Simulated Critical Reviewer
**Paper**: Self-Verification for Chain-of-Thought Reasoning

---

## Summary

This paper proposes adding a self-verification step to chain-of-thought reasoning for math problems. The core idea is to train the model to check its own intermediate steps. Experiments on GSM8K show improvements over standard CoT. However, several critical issues regarding evaluation rigor and comparison fairness need to be addressed.

## Overall Rating

**Verdict**: Major Revision Required  
**Confidence**: 4/5

The core idea is reasonable and timely, but the experimental validation has significant weaknesses that must be fixed before publication.

---

## Critical Issues (Must Fix)

### C1: Unfair Baseline Comparison
**Location**: Section 4 (Experiments)

**Issue**: The baseline (Standard CoT) is trained on the full training set, while your method uses additional verification data synthesized from the same set. This gives your method more effective training signal.

**Impact**: The reported 6.7 point improvement may be inflated due to this data advantage rather than the method itself.

**Evidence**: 
- Baseline: "trained on GSM8K train set" (Section 4.1)
- Your method: "synthetic verification data generated from GSM8K" (Section 3.2)
- No discussion of data size equivalence

**Fix**: 
- Train baseline with equivalent amount of data
- Or: ablate to show improvement comes from verification, not just more data
- Or: clearly acknowledge and bound this limitation

### C2: No Statistical Significance Testing
**Location**: Table 1

**Issue**: Results reported as single numbers (85.2% vs 78.5%) with no indication of variance across random seeds.

**Impact**: The 6.7 point difference might not be statistically significant. Could be due to lucky seed.

**Fix**:
- Run with 5-10 different random seeds
- Report mean ± standard deviation
- Perform statistical significance test (t-test)
- Show confidence intervals

---

## Major Issues (Should Fix)

### M1: Missing Critical Ablation
**Location**: Experiments

**Issue**: No ablation showing contribution of individual components:
- Verification module alone
- Reranking alone  
- Full pipeline

Without this, we don't know what actually drives the improvement.

**Fix**: Add Table X showing:
- Baseline: 78.5%
- + Verification only: X%
- + Reranking only: Y%
- + Both (full): 85.2%

### M2: Limited Evaluation Scope
**Location**: Section 4

**Issue**: Only evaluated on GSM8K. No evidence this generalizes to:
- Other math datasets (MATH, SVAMP)
- Different problem types
- Different model sizes

**Fix**:
- Add at least one more dataset (MATH is standard)
- Or: acknowledge limitation and scope claim to GSM8K

### M3: Overclaiming in Abstract
**Location**: Abstract, Line 3

**Issue**: "reducing arithmetic errors by 35%" - this is misleading.

The 35% is relative reduction in error rate (100-85.2)/(100-78.5) - 1 = ~35%, but the absolute improvement is only 6.7 points.

**Fix**: Report clearly: "improves accuracy from 78.5% to 85.2% (+6.7 points, 35% relative error reduction)"

---

## Minor Issues

### m1: Figure 2 Unclear
**Location**: Figure 2, Page 4

The architecture diagram is too small. Verification module details are unreadable. Legend confusing.

**Fix**: Redraw with larger font, clearer annotations.

### m2: Typo in Table 1 Caption
**Location**: Table 1

"Comparision" → "Comparison"

### m3: Missing Citation
**Location**: Section 2, Line 2

You mention "prior work in verification" but don't cite specific papers. Add citations to [X], [Y].

---

## Positive Aspects

1. **Timely problem**: Math reasoning is hot topic, verification is understudied
2. **Clean motivation**: Error analysis showing arithmetic mistakes is compelling
3. **Interpretable**: Verification scores provide insight into model uncertainty
4. **Well-written**: Generally clear and easy to follow

---

## Action Items (Prioritized)

### Critical Priority
- [ ] **C1**: Re-run baseline with fair data comparison
- [ ] **C2**: Add statistical significance testing (5+ seeds)

### High Priority  
- [ ] **M1**: Add component ablation study
- [ ] **M2**: Evaluate on MATH dataset
- [ ] **M3**: Fix overclaiming in abstract

### Medium Priority
- [ ] **m1**: Redraw Figure 2
- [ ] **m2**: Fix typo
- [ ] **m3**: Add missing citations

---

## Recommendation

**Major Revision Required**

The core idea is solid, but the experimental validation has critical flaws (C1, C2) that cast doubt on the main claims. These must be addressed. The additional major issues (M1-M3) should also be fixed to strengthen the paper.

I am willing to review a revised version. With these fixes, this could be a strong paper.

---

## Next Steps for Authors

1. Address C1 and C2 first (these are blockers)
2. Run new experiments with proper statistical rigor
3. Add ablation study to understand what works
4. Soften claims to match evidence
5. Fix presentation issues

After addressing these, I recommend running another internal review round before submitting to a real venue.
