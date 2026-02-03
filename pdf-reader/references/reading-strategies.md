# Efficient Paper Reading Strategies

## The 3-Pass Approach

### Pass 1: 5-Minute Scan (Pages 1-2)

**Goal**: Categorize the paper

**What to extract**:
1. **Category**: Theory? Empirical? Method? Application?
2. **Context**: What problem? Which area?
3. **Novelty**: What's new? (check contributions bullet points)
4. **Correctness**: Do assumptions make sense?
5. **Clarity**: Well written?

**Decision**: Continue to Pass 2 or discard?

### Pass 2: 30-Minute Understanding (Key Sections)

**Goal**: Understand content without details

**Focus on**:
- **Figures, diagrams, illustrations** (get the big picture)
- **Section headings** (understand flow)
- **Results summary** (check if claims are supported)

**Note**: Skip proofs, derivations, implementation details.

### Pass 3: Deep Dive (Full Paper)

**Goal**: Full understanding

**When to do this**:
- Paper is highly relevant to your work
- You're implementing their method
- You're reviewing/citing it

**Focus**: Every detail that matters for your purpose.

---

## AI-Assisted Reading with PDF Images

### Pass 1 (Automated)

```bash
# Convert just first 2 pages
uv run python scripts/convert.py --arxiv ID --pages 1-2 --output ./pass1/

# AI reads page_001.png, page_002.png
# Extracts: title, abstract, contributions
# Classifies: relevant / maybe / not relevant
```

### Pass 2 (Semi-Automated)

```bash
# Find and convert key figures/tables
# AI scans pages, identifies which contain figures
uv run python scripts/convert.py --arxiv ID --pages 1,2,4,5,8 --output ./pass2/

# AI reads:
# - page_001: Title/context
# - page_002: Problem/approach
# - page_004-005: Method figures
# - page_008: Results table
```

### Pass 3 (Manual + AI)

```bash
# Full conversion if needed
uv run python scripts/convert.py --arxiv ID --output ./full/

# Human: Reads deeply, takes notes
# AI: Helps extract specific information on request
```

---

## What to Look For

### For Literature Review
- Problem definition (how do they frame it?)
- Key related work (who do they cite?)
- Limitations (what do they acknowledge?)

### For Baseline Comparison
- Exact experimental setup (dataset split? hyperparameters?)
- Metrics used (accuracy? F1? something custom?)
- Numerical results (main table)
- Ablation studies (what matters?)

### For Method Inspiration
- Architecture diagrams
- Algorithm pseudocode
- Key equations/formulas
- Implementation details (appendix?)

### For Writing Your Paper
- How they structure Introduction
- How they describe related work
- Figure/table styles
- Citation patterns

---

## Quick Reference: Page Types

| Page Type | What to Extract | Priority |
|-----------|-----------------|----------|
| Title page | Title, authors, abstract | High |
| Introduction | Problem, motivation, contributions | High |
| Related Work | Key citations, how they differ | Medium |
| Method | Architecture, algorithm, formulas | High |
| Experiments | Setup, results, ablations | High |
| Conclusion | Summary, limitations, future | Low |
| Appendix | Details, proofs, extra results | As needed |
| References | Who they cite | For snowballing |

---

## Common Patterns

### Standard ML Paper Structure
```
Page 1:    Title, Abstract
Page 2-3:  Introduction (last para = contributions)
Page 4-5:  Related Work
Page 6-8:  Method (Figure 1 = architecture)
Page 9-11: Experiments (Tables 1-2 = main results)
Page 12:   Conclusion, References
```

### Multi-Modal Paper
```
Page 1-2:  Title, Abstract (mentions vision + language)
Page 3-4:  Introduction (task, challenges)
Page 5:    Related Work (split: vision, NLP, multi-modal)
Page 6-9:  Method (Figure 1 = model, Figure 2 = attention)
Page 10-12: Experiments (multiple datasets)
Page 13:   Qualitative results (example outputs)
```

### Theory Paper
```
Page 1-2:  Title, Abstract (theorem mentioned)
Page 3:    Introduction (problem + main theorem)
Page 4-6:  Related Work + Preliminaries
Page 7-10: Theory (definitions, lemmas, main proof)
Page 11-12: Empirical validation (if any)
Page 13:   Discussion
```

---

## Tips for AI Analysis

### When Reading Images

**Ask AI to**:
1. Transcribe text (title, abstract, key sentences)
2. Describe figures (what's shown? axes? trends?)
3. Extract tables (copy numbers carefully)
4. Identify formulas (transcribe in LaTeX if possible)

**Verify**:
- Check numbers make sense (ballpark estimate)
- Ensure you didn't miss negative signs or units
- Confirm table headers are interpreted correctly

### Handling Unclear Content

If image quality is poor:
- Try higher zoom: `--zoom 3`
- Ask AI to "best effort" interpret
- Note uncertainty: "Value appears to be 92.3 but unclear"
- Cross-reference with abstract or text

---

## Time Budget

| Task | Time | Pages |
|------|------|-------|
| Quick relevance check | 5 min | 1-2 |
| Understand approach | 15 min | 3-6 |
| Detailed analysis | 45 min | Key sections |
| Full deep dive | 2-3 hours | All |

Use PDF images strategically—don't convert everything if you don't need to.
