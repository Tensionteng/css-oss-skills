---
name: pdf-reader
description: Convert PDF papers to images for AI analysis. Extract figures, tables, formulas, and text layout.
metadata:
  author: tengshiyuan
  tags: [PDF, Papers, Literature Review, Figures]
  dependencies: [pymupdf]
---

# PDF Reader

Convert academic papers (PDF) to images for AI analysis. This enables multi-modal models to "read" papers by viewing pages as images, preserving visual information like figures, tables, formulas, and layout.

## Quick Start

```bash
# Convert arXiv paper to images
uv run python scripts/convert.py --arxiv 2405.12345 --output ./paper-images/

# Convert specific pages only
uv run python scripts/convert.py --arxiv 2405.12345 --pages 1,3,5-10 --output ./key-pages/

# Extract embedded figures only (high-res)
uv run python scripts/convert.py --arxiv 2405.12345 --figures-only --output ./figures/

# Convert local PDF
uv run python scripts/convert.py --pdf /path/to/paper.pdf --output ./images/
```

Then use `ReadMediaFile` to analyze the generated images.

---

## Core Workflow

### Step 1: Convert PDF to Images

**For quick scan** (first few pages):
```bash
uv run python scripts/convert.py \
    --arxiv 2405.12345 \
    --pages 1-3 \
    --output .research/papers/paper-1/
```

**For deep analysis** (full paper):
```bash
uv run python scripts/convert.py \
    --arxiv 2405.12345 \
    --output .research/papers/paper-1/ \
    --zoom 2
```

**For figures only** (extract embedded images):
```bash
uv run python scripts/convert.py \
    --pdf paper.pdf \
    --figures-only \
    --output .research/papers/paper-1/figures/
```

### Step 2: Analyze with AI

Use `ReadMediaFile` to read specific pages:

```python
# Read title page
ReadMediaFile(path=".research/papers/paper-1/page_001.png")

# Read method figure
ReadMediaFile(path=".research/papers/paper-1/page_004.png")

# Read results table
ReadMediaFile(path=".research/papers/paper-1/page_006.png")
```

### Step 3: Extract Information

When analyzing images, focus on:

**Title Page (page_001)**:
- Paper title
- Authors and affiliations
- Abstract
- Keywords

**Introduction (page_002-003)**:
- Problem statement
- Motivation
- Main contributions (often bulleted)

**Method Section**:
- Architecture diagrams (Figure 1, 2...)
- Algorithm pseudocode
- Key formulas
- Model structure

**Experiments Section**:
- Main results table (record numbers carefully)
- Comparison with baselines
- Ablation studies
- Performance curves

**Figures/Tables**:
- Extract specific values
- Understand axes and units
- Note statistical significance markers

---

## When to Use

### From research-brainstorming
**Quick relevance check**: Convert first 2-3 pages to quickly assess if paper is relevant.

```bash
uv run python scripts/convert.py --arxiv ID --pages 1-3 --output ./quick/
```

### From research-execution
**Baseline analysis**: Convert full paper or method+experiment sections.

```bash
# Method + experiments (typical location)
uv run python scripts/convert.py --arxiv ID --pages 1,2,3,4,5,8,9,10 --output ./baseline/
```

### From manuscript-writing
**Related Work**: Convert papers to extract key citations and comparisons.

```bash
# Extract figures for your paper
uv run python scripts/convert.py --pdf ref.pdf --figures-only --output ./ref-figures/
```

---

## Options Reference

### convert.py

| Option | Description | Example |
|--------|-------------|---------|
| `--arxiv ID` | arXiv paper ID | `--arxiv 2405.12345` |
| `--pdf PATH` | Local PDF path | `--pdf ./paper.pdf` |
| `--output DIR` | Output directory (required) | `--output ./images/` |
| `--pages RANGE` | Specific pages (1-based) | `--pages 1,3,5-10` |
| `--zoom N` | Resolution (1=72dpi, 2=144dpi, 3=216dpi) | `--zoom 2` |
| `--figures-only` | Extract embedded figures only | `--figures-only` |

**Default**: All pages, zoom=2 (144dpi), PNG format

---

## Best Practices

### Start Small
Don't convert 50-page papers entirely. Start with key pages:
1. Page 1: Title/Abstract
2. Find method section (scan middle pages)
3. Find experiments section
4. Convert only relevant pages

### Zoom Level
- `--zoom 1`: Fast, smaller files, good for text
- `--zoom 2` (default): Balanced, recommended for most cases
- `--zoom 3`: High quality, better for complex figures, larger files

### Page Selection
Common patterns:
```bash
# Title + Abstract + Intro
--pages 1-3

# Title + Abstract + Method figure + Results table
--pages 1,2,4,8

# Just the figures (look for pages with large images)
--pages 3,5,7,10
```

### Storage
Images can be large. Recommend:
- Store in `.research/papers/` (already gitignored usually)
- Delete after analysis if space is concern
- Or keep for future reference

---

## Limitations

1. **No text extraction**: Use images + AI vision, not copy-paste text
2. **Formula readability**: Depends on PDF quality; zoom 3 may help
3. **Large PDFs**: >100 pages may take time and space
4. **No semantic understanding**: AI must interpret visual layout

---

## Common Issues

**Issue: arXiv download fails**
```
Error: 404 Not Found
```
Check arXiv ID format. Should be like `2405.12345` or `2405.12345v1`.

**Issue: Permission denied on /tmp/**
Use `--output` to specify a writable directory.

**Issue: Images are blurry**
Increase zoom: `--zoom 3`

**Issue: Figures look weird**
Some PDFs have vector figures that don't render well. Try `--figures-only` to extract original embedded images.

---

## Integration Examples

### Example 1: Quick Paper Assessment

```bash
# Convert first 3 pages
uv run python scripts/convert.py --arxiv 2405.12345 --pages 1-3 --output ./quick/

# AI then reads:
# - page_001.png: "This paper is about X, uses method Y..."
# - page_002.png: "They claim contribution Z..."
# Decision: Relevant or not?
```

### Example 2: Baseline Analysis

```bash
# Convert key sections
uv run python scripts/convert.py --arxiv 2405.12345 --output ./baseline/

# AI analyzes:
# 1. Read page_001-003: Understand problem and approach
# 2. Scan pages to find "Method" section (e.g., page_004.png)
# 3. Scan pages to find "Experiments" section (e.g., page_008.png)
# 4. Extract SOTA numbers from table in page_008.png
# 5. Record: {"method": "X", "metric": "Y", "value": "Z"}
```

### Example 3: Extract Figures for Your Paper

```bash
# Get high-res figures from reference
uv run python scripts/convert.py --pdf reference.pdf --figures-only --output ./ref-figures/

# Review images, potentially use as inspiration for your figures
```

---

## References

- **PDF quality tips**: [references/pdf-quality.md](references/pdf-quality.md)
- **Efficient paper reading**: [references/reading-strategies.md](references/reading-strategies.md)
- **Extracting data from tables**: [references/table-extraction.md](references/table-extraction.md)
