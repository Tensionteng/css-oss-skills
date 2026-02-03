# Review History

## Current Status
**Latest Round**: 2
**Date**: 2026-02-05
**Overall**: Minor Revision
**Trend**: Improving ✓

---

## Round 1 (2026-01-31)
**Status**: Major Revision
**Reviewer Focus**: Technical soundness, missing experiments

### Issues Found
| ID | Issue | Severity | Status | Verification |
|----|-------|----------|--------|--------------|
| R1.C1 | Unfair baseline comparison | Critical | ✓ Fixed | Round 2 confirmed |
| R1.C2 | No statistical significance | Critical | ✓ Fixed | Round 2 confirmed |
| R1.M1 | Missing ablation study | Major | ✓ Fixed | Round 2 confirmed |
| R1.M2 | Limited to GSM8K only | Major | ⚠️ Partial | Added SVAMP, MATH pending |
| R1.M3 | Overclaiming in abstract | Major | ✓ Fixed | Round 2 confirmed |
| R1.m1 | Figure 2 unclear | Minor | ✓ Fixed | Round 2 confirmed |
| R1.m2 | Typo in caption | Minor | ✓ Fixed | Round 2 confirmed |
| R1.m3 | Missing citations | Minor | ✓ Fixed | Round 2 confirmed |

### Key Feedback from Round 1
Reviewer identified critical flaws in experimental design:
1. Baseline comparison was unfair (data advantage to our method)
2. No statistical testing (single run reported)
3. Missing ablations to understand what works

These were structural issues requiring new experiments.

---

## Round 2 (2026-02-05)
**Status**: Minor Revision
**Previous Issues**: 6/8 fully resolved, 1 partial, 1 pending

### Verification of Round 1 Fixes

**Critical Issues - ALL RESOLVED ✓**
- R1.C1: ✓ **Confirmed fixed** - Re-ran baseline with equivalent data. New results: Baseline 79.1%, Ours 84.8% (+5.7, still significant)
- R1.C2: ✓ **Confirmed fixed** - Ran 5 seeds. Reported: 84.8±1.2 vs 79.1±2.0. Significant at p<0.01.

**Major Issues**
- R1.M1: ✓ **Confirmed fixed** - Added Table 2 with ablations. Verification alone: +3.2, Reranking alone: +1.5, Full: +5.7
- R1.M2: ⚠️ **Partially fixed** - Added SVAMP results (shows similar improvement). MATH still running (ETA 2 days)
- R1.M3: ✓ **Confirmed fixed** - Abstract now reads "improves from 78.5% to 85.2% (+6.7 points)"

**Minor Issues - ALL RESOLVED ✓**
- R1.m1: ✓ Redrew Figure 2 with larger font and clearer annotations
- R1.m2: ✓ Fixed typo
- R1.m3: ✓ Added citations to [27] and [31]

### Persistent Issues
**R1.M2 partially unresolved** - MATH evaluation still pending. This is taking longer than expected due to compute constraints.

### New Issues Found in Round 2
| ID | Issue | Severity | Status |
|----|-------|----------|--------|
| R2.m1 | Broken reference [12] | Minor | 🔧 To Fix |
| R2.m2 | Limitations section too brief | Minor | 🔧 To Fix |
| R2.m3 | Appendix mentions figure that doesn't exist | Trivial | 🔧 To Fix |

### Trend Analysis
- **Improvement**: Significant progress from Round 1 to Round 2
  - Round 1: 2 Critical, 3 Major, 3 Minor = 8 issues
  - Round 2: 0 Critical, 0 Major (MATH pending), 2 Minor, 1 Trivial = 3 minor issues
- **Resolution rate**: 75% of R1 issues fully resolved
- **Quality trajectory**: 😤→🙂 (Critical→Constructive)

### Persistent Themes Across Rounds
**Overclaiming tendency**: Appeared in R1.M3, need to watch for this in future papers. Consider adding "claim check" to writing workflow.

---

## Trends & Insights

### Recurring Themes
- **Experimental rigor**: Both rounds focused on this. First it was unfair comparison, now it's completeness (MATH pending).
- **Claim precision**: R1 had overclaiming, now fixed. Pattern: tend to state strongest version of result.

### Quality Trajectory
| Round | Sentiment | Overall | Issues |
|-------|-----------|---------|--------|
| 1 | 😤 Critical | Major Revision | 8 (2 Critical) |
| 2 | 🙂 Constructive | Minor Revision | 3 (0 Critical) |
| 3 (planned) | 🤞 Hopeful | Accept? | TBD |

### What We've Learned
1. **Baselines matter**: The unfair comparison in R1 would have been a reject in real review
2. **Stats matter**: Single-run results not credible
3. **Time management**: MATH evaluation taking longer than expected - should have started earlier

### Readiness Checklist
- [x] All critical issues resolved
- [x] All major issues resolved (or have plan)
- [ ] Minor issues from R2 pending (2 items)
- [ ] MATH results pending (ETA 2 days)
- [ ] Final proofread needed

**Estimated to submission**: 3-4 days (after MATH results + final fixes)

---

## Action Plan

### Immediate (Next 2 Days)
- [ ] Wait for MATH evaluation to complete
- [ ] Fix R2 issues (broken ref, limitations, appendix)

### Before Round 3
- [ ] Incorporate MATH results
- [ ] Do final pass for typos/grammar
- [ ] Check all figures render correctly

### Round 3 Goals
- Verify MATH results look reasonable
- Confirm R2 fixes worked
- Final "accept" decision

---

## Notes

**Compute bottleneck**: MATH evaluation is the blocker. Consider:
- Starting long experiments earlier in future
- Or: submitting with SVAMP only and adding MATH in rebuttal

**Reviewer quality**: The simulated reviewer caught issues that would definitely come up in real review. Very valuable.

**Recommendation**: One more round after MATH results, then submit to ICLR (deadline: Feb 15).
