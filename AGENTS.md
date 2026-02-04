# AGENTS.md

This file provides essential context for AI coding agents working with this repository. The project follows the [Anthropic Agent Skills](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview) framework.

## Project Overview

**AI Research Assistant Skills Library** - A curated collection of modular AI research skills for Claude Code and the Claude Agent SDK. Each skill packages domain-specific expertise, workflows, and tools to enable AI agents to assist with academic research tasks.

**Mission**: Provide expert-level guidance for AI research activities, from initial idea brainstorming to publication-ready manuscript writing.

**License**: MIT

## Repository Structure

```
.
├── manuscript-writing/          # Skill: ML paper writing for top conferences
│   ├── SKILL.md                # Main skill instructions (937 lines)
│   ├── references/             # Deep documentation
│   │   ├── writing-guide.md    # Writing philosophy & principles
│   │   ├── citation-workflow.md# Citation verification APIs
│   │   ├── checklists.md       # Conference submission checklists
│   │   ├── reviewer-guidelines.md
│   │   └── sources.md          # Bibliography
│   ├── scripts/                # (none in this skill)
│   └── templates/              # LaTeX templates
│       ├── neurips2025/
│       ├── icml2026/
│       ├── iclr2026/
│       ├── acl/
│       ├── aaai2026/
│       └── colm2025/
├── research-brainstorming/     # Skill: Research ideation & validation
│   ├── SKILL.md                # Main skill instructions (317 lines)
│   ├── references/
│   │   ├── conversation-patterns.md
│   │   ├── evaluation-rubric.md
│   │   ├── literature-search.md
│   │   └── examples/
│   │       └── IDEA-example-1.md  # Example IDEA.md file
│   └── scripts/                # Literature scanning tools
│       ├── arxiv_scan.py       # arXiv API search script
│       └── s2_scan.py          # Semantic Scholar search script
├── anthropic_official_docs/    # Anthropic's skill authoring guidelines
│   ├── best_practices.md       # Comprehensive skill authoring guide
│   └── skills_overview.md      # How skills work
├── docs/
│   └── SKILL_TEMPLATE.md       # Template for creating new skills
├── CLAUDE.md                   # Detailed project documentation (303 lines)
├── LICENSE                     # MIT License
└── .gitignore                  # Python/ML focused gitignore
```

## Technology Stack

- **Skill Format**: Markdown with YAML frontmatter
- **Scripts**: Python 3 (arxiv, semanticscholar, requests, habanero packages)
- **Templates**: LaTeX for academic paper templates
- **Version Control**: Git
- **License**: MIT

## Skill Format Specification

Every skill MUST follow this structure:

### YAML Frontmatter (Required)

```yaml
---
name: skill-name-here              # kebab-case, 64 chars max, no "anthropic"/"claude"
description: Third-person description of what AND when to use this skill
version: 1.0.0                     # Semantic versioning
author: Your Name                  # For marketplace badges
license: MIT                       # Standard license
tags: [Tag One, Tag Two]          # Title Case (UPPERCASE for acronyms like GRPO, TRL)
dependencies: [pkg>=1.0.0]         # Optional, with version constraints
---
```

**Critical Rules**:
- `name`: Use gerund form (e.g., `serving-llms`, `processing-data`, `brainstorming-research`)
- `description`: Third person, max 1024 chars, no XML tags, include WHAT and WHEN
- `tags`: Title Case for words, UPPERCASE for acronyms
- No quotes around field values (except in arrays)

### SKILL.md Body Standards

- **Length**: 200-500 lines maximum (critical for performance)
- **Style**: Assume Claude is smart, no over-explaining basics
- **Point of view**: Third person ("Use this skill when...")
- **Code blocks**: MUST include language tags (```python, ```bash, etc.)
- **Workflows**: Include copy-paste checklists for complex tasks
- **References**: Link to files in `references/` directory (one level deep only)

### Directory Structure

```
skill-name/
├── SKILL.md                    # Main instructions (required)
├── references/                 # Deep documentation (optional)
│   ├── README.md
│   ├── api.md
│   ├── tutorials.md
│   └── ...
├── scripts/                    # Helper scripts (optional)
│   └── utility.py
└── templates/                  # Code templates (optional)
```

## Key Development Conventions

### Naming Conventions

- **Skill names**: Gerund form (verb + -ing) in kebab-case
  - ✅ `processing-pdfs`, `writing-papers`, `brainstorming-research`
  - ❌ `pdf-helper`, `paper-tools`, `research-utils`
- **Files**: Use kebab-case for markdown files
- **Scripts**: Use snake_case for Python files

### Progressive Disclosure

SKILL.md serves as an overview pointing to detailed materials:

```markdown
## Advanced Features

**API Reference**: See [references/api.md](references/api.md)
**Troubleshooting**: See [references/issues.md](references/issues.md)
```

**NEVER nest references** (SKILL.md → ref1.md → ref2.md). Keep all reference links one level deep from SKILL.md.

### Code Examples

Always use language detection:

```python
# Good - has language tag
import requests
```

NOT:

```
# Bad - no language tag
import requests
```

## Quality Validation

Before adding or modifying skills, validate:

```bash
# Check YAML frontmatter exists and is valid
head -20 skill-name/SKILL.md
python -c "import yaml; yaml.safe_load(open('skill-name/SKILL.md').read().split('---')[1])"

# Verify SKILL.md line count (MUST be 200-500 lines)
wc -l skill-name/SKILL.md

# Check documentation size (target 300KB+ for references/)
du -sh skill-name/references/

# Verify code blocks have language tags
grep -A 1 '```' skill-name/SKILL.md | head -20
```

## Adding a New Skill

1. **Create directory** with kebab-case name
2. **Copy template** from `docs/SKILL_TEMPLATE.md`
3. **Write SKILL.md** following the format above
4. **Add references/** if additional documentation needed
5. **Add scripts/** if utility tools are needed
6. **Validate quality** using commands above
7. **Test** the skill with real use cases

Example:

```bash
# Create new skill
mkdir my-new-skill
cp docs/SKILL_TEMPLATE.md my-new-skill/SKILL.md

# Edit SKILL.md with your content
# Add references/, scripts/ as needed

# Validate
wc -l my-new-skill/SKILL.md  # Should be 200-500
du -sh my-new-skill/references/  # Should be substantial
```

## Git Workflow

```bash
# Create feature branch
git checkout -b add-skill-name

# Add skill directory
git add skill-name/

# Commit with descriptive message
git commit -m "Add [Skill Name] skill

- X lines of documentation
- Y references included
- Scripts for Z functionality"

# Push and create PR
git push origin add-skill-name
```

## Testing Skills

Skills should be tested with Claude Code or Agent SDK:

1. **Place skill in skills directory**:
   - Claude Code: `~/.claude/skills/` or project `.claude/skills/`
   - Agent SDK: `.claude/skills/`

2. **Trigger the skill**:
   ```
   /skill:skill-name
   "Test query relevant to the skill"
   ```

3. **Verify behavior**:
   - Skill activates when expected
   - Instructions are clear and actionable
   - References load correctly
   - Scripts execute properly

## Dependencies

Some skills require Python packages:

**manuscript-writing**:
```bash
pip install semanticscholar arxiv habanero requests
```

**research-brainstorming**:
```bash
pip install arxiv semanticscholar
```

## Key Files Reference

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Comprehensive project documentation and standards |
| `docs/SKILL_TEMPLATE.md` | Copy-paste template for new skills |
| `anthropic_official_docs/best_practices.md` | Anthropic's official skill authoring guide |
| `anthropic_official_docs/skills_overview.md` | How skills work conceptually |
| `.gitignore` | Python/ML focused ignore patterns |

## Common Tasks

### Update an existing skill

1. Edit SKILL.md maintaining YAML frontmatter
2. Keep line count under 500 (split to references/ if needed)
3. Update version number in frontmatter
4. Test changes

### Add reference documentation

1. Create file in `skill-name/references/`
2. Link from SKILL.md (one level deep)
3. Include table of contents for files >100 lines
4. Target 300KB+ total for references/ directory

### Add utility scripts

1. Create in `skill-name/scripts/`
2. Include shebang (`#!/usr/bin/env python3`)
3. Add argparse for CLI usage
4. Document in SKILL.md with usage examples
5. Handle errors explicitly (don't punt to Claude)

## Anti-patterns to Avoid

- ❌ SKILL.md over 500 lines
- ❌ Over-explaining basics ("Python is a programming language...")
- ❌ First-person descriptions ("I can help you...")
- ❌ Vague skill names ("helper", "utils", "tools")
- ❌ Nested references (SKILL.md → A.md → B.md)
- ❌ Windows-style paths (`scripts\file.py`)
- ❌ Missing code language tags
- ❌ First-person YAML descriptions

## Resources

- **Anthropic Skills Docs**: https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview
- **Best Practices**: See `anthropic_official_docs/best_practices.md`
- **Template**: See `docs/SKILL_TEMPLATE.md`
- **Project Docs**: See `CLAUDE.md` for full project details
