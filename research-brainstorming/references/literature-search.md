# Literature Search Strategies

## Quick Scan (5-10 minutes)

Use this during brainstorming sessions for rapid feasibility assessment.

### arXiv Search Strategy

**Best for**: Latest preprints, CS/ML topics

```bash
# Basic search
python scripts/arxiv_scan.py "your keywords" --max-results 10

# Recent work only
python scripts/arxiv_scan.py "your keywords" --max-results 10 --days 365

# Specific category
python scripts/arxiv_scan.py "cat:cs.CL AND your keywords" --max-results 10
```

**Key arXiv categories**:
- `cs.CL`: Computation and Language (NLP)
- `cs.LG`: Machine Learning
- `cs.AI`: Artificial Intelligence
- `cs.CV`: Computer Vision

### Semantic Scholar Strategy

**Best for**: Citation context, broader coverage

```bash
python scripts/s2_scan.py "your keywords" --max-results 10
```

**Advantages**:
- Includes non-arXiv papers (conferences, journals)
- Citation counts for impact assessment
- Fields of study for landscape analysis

---

## Search Query Formulation

### From vague to specific

| Vague | Better | Best |
|-------|--------|------|
| "LLM reasoning" | "chain of thought reasoning" | "chain of thought arithmetic reasoning errors" |
| "improve transformers" | "efficient attention mechanisms" | "linear attention approximation transformers" |
| "better embeddings" | "contrastive learning embeddings" | "hard negative mining contrastive sentence embeddings" |

### Query templates

**Finding similar work**:
```
"[method name]" [task domain]
```
Example: `"chain of thought" math word problems`

**Finding surveys**:
```
"[topic]" (survey OR review OR "state of the art")
```
Example: `large language model reasoning survey`

**Finding gaps**:
```
"[method]" (limitation OR challenge OR problem)
```
Example: `chain of thought limitation`

**Finding datasets/benchmarks**:
```
"[task]" dataset benchmark evaluation
```
Example: `mathematical reasoning dataset benchmark`

---

## Assessing Search Results

### Red flags (crowded space)

- >20 highly relevant papers in last 2 years
- Multiple survey papers exist
- Top papers have 1000+ citations

**Response**: Need strong differentiation or niche angle

### Red flags (empty space)

- <3 relevant papers
- Papers are very old (>5 years)
- No recent arXiv preprints

**Response**: Verify problem is real, check adjacent keywords

### Green flags (sweet spot)

- 5-15 relevant papers
- Mix of established and recent work
- Clear limitations mentioned in abstracts
- No single dominant approach

**Response**: Good landscape—look for specific gaps

---

## Deep Dive Strategies

When you need more than a quick scan:

### Citation tracing

1. Find 2-3 most relevant papers
2. Check their related work sections
3. Look at papers they cite (backward)
4. Look at papers citing them (forward)

### Author tracking

- Identify key authors in the space
- Check their recent publications
- Look for their workshop/tutorial talks

### Venue analysis

- Which conferences publish this work?
- Are there dedicated workshops?
- Track upcoming deadlines for relevant venues

---

## Integrating with .research/IDEA.md

After each search, update `.research/IDEA.md`:

```markdown
## Literature Scan

- **Keywords tried**: [list queries]
- **Key papers**:
  - [Title] ([id]): [Why relevant]
  - [Title] ([id]): [Why relevant]
- **Landscape**: [crowded/active/emerging/sparse]
- **Gap identified**: [What's missing]
- **Opportunity**: [Your potential angle]
```
