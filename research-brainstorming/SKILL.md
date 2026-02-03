---
name: research-brainstorming
description: Guide researchers through structured brainstorming to transform vague ideas into viable angles. Maintains .research/IDEA.md as shared documentation.
tags: [Research, Brainstorming, Idea Validation, Academic Writing]
dependencies: [arxiv, semanticscholar]
---

# Research Brainstorming

Guide researchers through structured brainstorming to transform vague ideas into viable research angles. This is a **conversational** skill—interact with the researcher through multiple turns while maintaining a shared `.research/IDEA.md` file as the "single source of truth."

## Quick Start

```bash
# First time: Initialize brainstorming session
/skill:research-brainstorming
"I want to brainstorm about [your topic]"

# Continue existing session
/skill:research-brainstorming
"Let's continue our discussion"
```

**What happens:**
1. Check for `.research/` directory, create if needed
2. Read existing `.research/IDEA.md` (if any)
3. Guide structured conversation
4. Update `.research/IDEA.md` with new insights
5. Continue until a viable angle emerges

---

## Core Workflow

### Session Flow

```
[Start] → Check/Create .research/ → Read .research/IDEA.md → Check-in → Explore → Update .research/IDEA.md → [End]
                              ↑___________________________↓
                                    (repeat as needed)
```

### Before Each Session

1. **Ensure `.research/` directory exists**
   - Check: `ls -la .research/`
   - If not exists: `mkdir -p .research/`

2. **Read `.research/IDEA.md`** (if exists)
   - Check `status`: exploring / refining / viable / paused
   - Review `iteration` count
   - Note `open questions`
   - Understand `current angle`

3. **Check-in with researcher**
   - "Based on `.research/IDEA.md`, we're at [status], iteration [N]"
   - "Last time we discussed [summary]"
   - "Any new thoughts, or shall we tackle [open question]?"

### During Session

**Phase 1: Idea Extraction**
- Ask open questions to extract the researcher's thoughts
- Listen for: vague terms, implicit assumptions, hidden constraints
- Don't judge, just explore

**Phase 2: Quick Validation** (when needed)
- Run 5-minute literature scan using scripts
- Report: "I found X papers... This angle seems [novel/overcrowded]"
- Ask: "How does your approach differ from [specific paper]?"

**Phase 3: Refinement**
- Iterate on the angle until it's crisp
- Identify open questions
- Assess feasibility

### End of Session

**Update `.research/IDEA.md`:**
- Add new exploration entry to `iteration history`
- Update `current angle` if changed
- Refresh `open questions` list
- Update `viability assessment`
- Increment `iteration` counter
- Set `next action`

**Confirm with researcher:**
- "I've updated `.research/IDEA.md` with our discussion"
- "Next time we can focus on [next action]"

---

## .research/IDEA.md Template（中文撰写）

在 `.research/IDEA.md` 创建以下内容（使用中文）：

```markdown
---
status: exploring  # exploring / refining / viable / paused
iteration: 1
last_updated: 2026-01-30
---

# 研究想法: [一句话标题]

## 当前角度

**一句话描述**: [能用一句话说清楚吗？]

**问题**: [解决什么具体问题？]
**核心洞察**: [关键直觉是什么？]
**方法**: [打算怎么解决？]
**差异化**: [和现有工作有什么不同？]

## 迭代历史

### 迭代 1 (2026-01-30)
- **探索**: [探索了哪个方面？]
- **发现**: [学到了什么？]
- **决策**: [继续 / 调整 / 放弃]

## 待解决问题

- [ ] [问题 1]: [描述] (优先级: 高)
- [ ] [问题 2]: [描述] (优先级: 中)

## 文献检索

- **尝试的关键词**: [搜索词]
- **关键论文**:
  - [标题] ([arxiv id]): [相关性评估]
- **发现的空白**: [现有工作缺少什么？]

## 可行性评估

| 维度 | 评分 (1-5) | 备注 |
|------|-----------|------|
| 创新性 | - | [待填] |
| 可行性 | - | [待填] |
| 影响力 | - | [待填] |
| 清晰度 | - | [能解释清楚吗？] |

## 下一步行动

- [ ] [具体下一步，例如："确认baseline选择"]
```

---

## Conversation Guide

### Phase 1: Idea Extraction (Turns 1-2)

**Start with:**
> "Tell me what you're thinking about. Doesn't need to be complete—just dump your thoughts."

**Probing questions:**
- "What problem or observation sparked this?"
- "What would the ideal outcome look like?"
- "Why do you think this hasn't been solved well?"
- "Can you give me a concrete example?"

**Listen for red flags:**
- Vague terms: "improve", "better", "optimize" → Ask: "Specifically, what metric?"
- Broad scope: "fix NLP" → Ask: "What's the smallest interesting version?"
- Solution without problem: "Use Transformer" → Ask: "What problem does this solve?"

### Phase 2: Quick Literature Check (Turn 3-4)

**When to do this:**
- After extracting the core idea
- Before going too deep into details

**Use the script:**
```bash
python scripts/arxiv_scan.py "your search query" --max-results 5
```

**Report findings:**
> "I scanned arXiv for [keywords]. Found:
> - [Paper 1]: Very similar to your idea
> - [Paper 2]: Related but different angle
> 
> **Assessment**: This space has [X] activity. Your differentiation could be [Y]."

### Phase 3: Refinement Loop (Turn 5+)

**Continue until:**
- ✅ Can explain the angle in one crisp sentence
- ✅ Know how it's different from existing work
- ✅ Can describe the first experiment
- ✅ Researcher feels excited about it

**Common refinement patterns:**

| Issue | Response |
|-------|----------|
| Too broad | "What's the smallest version that would be interesting?" |
| Already done | "What aspect did they miss? Can we do it better/faster?" |
| Not novel | "What if we change the setting/method/metric?" |
| Unfeasible | "What's the 80/20 version that proves the concept?" |

---

## Status Transitions

### exploring → refining
When:
- A concrete angle emerges (not just "LLM reasoning" but "LLM reasoning errors on multi-step algebra")
- Basic feasibility confirmed (papers exist but gap identified)
- Can write 2-3 sentences describing the approach

### refining → viable
When:
- One-liner is crisp and clear
- Differentiation is defensible
- First experiment is obvious
- Overall viability score ≥ 3.5

### any → paused
When:
- Need information from researcher ("I need to check if we have the data")
- Need deeper literature review
- Researcher wants to think before continuing

---

## When to Use vs Alternatives

**Use this skill when:**
- "I have a vague idea..."
- "Is this worth pursuing?"
- "How should I frame this contribution?"
- "Help me narrow down my research direction"

**Use `research-execution` instead when:**
- Direction is clear, need to design experiments
- Need systematic literature review for Related Work
- Ready to start coding/collecting data

**Use `manuscript-writing` instead when:**
- Experiments are done, need to write paper
- Have results, need to structure the story

---

## Scripts

### arxiv_scan.py

Quick literature scan using arXiv API:

```bash
python scripts/arxiv_scan.py "chain of thought reasoning" --max-results 10 --days 365
```

Output: List of papers with relevance assessment.

### s2_scan.py

Semantic Scholar search for broader coverage:

```bash
python scripts/s2_scan.py "large language model math reasoning" --max-results 10
```

---

## Common Issues

**Issue: Researcher keeps changing direction**
> "Let's pick one angle and explore it deeply for 10 minutes. We can always pivot after that."

**Issue: Idea feels too big**
> "If you had to prove this concept in 2 weeks with minimal resources, what's the smallest version?"

**Issue: Can't find differentiation**
> "Let's list 3 existing approaches and identify what each misses. Can we combine or improve?"

**Issue: .research/IDEA.md becomes stale**
> Always update `.research/IDEA.md` during/after each session. If researcher references outdated info, correct it.

---

## Example Session

**Researcher:** "I want to do something with LLM reasoning"

**AI:** [Checks `.research/`, creates if needed, reads `.research/IDEA.md` - doesn't exist, creates new one]
> "Great! I've created `.research/IDEA.md` to track our exploration. Let's start simple: What specifically about LLM reasoning interests you? Is it accuracy, speed, interpretability, or something else?"

**Researcher:** "Accuracy. They make dumb mistakes on simple math."

**AI:** [Updates `.research/IDEA.md` - Current Angle]
> "Got it—math reasoning errors. Can you give me an example of the kind of mistake you mean?"

[... 5 minutes of discussion ...]

**AI:** [Updates `.research/IDEA.md` - Iteration 1]
> "Let me do a quick scan to see what's already been done in this space..."

[Runs arxiv_scan.py]

**AI:** [Updates `.research/IDEA.md` - Literature Scan]
> "I found several papers on LLM math reasoning. The key insight seems to be that chain-of-thought helps but isn't perfect. How would your approach differ?"

[... continues until angle is viable ...]

**AI:** [Final update to `.research/IDEA.md`]
> "I think we have a viable angle now. I've updated `.research/IDEA.md` with our final consensus: [summary]. Next session we can move to experiment design."

---

## References

- **Detailed conversation patterns**: [references/conversation-patterns.md](references/conversation-patterns.md)
- **Literature search strategies**: [references/literature-search.md](references/literature-search.md)
- **Idea evaluation rubric**: [references/evaluation-rubric.md](references/evaluation-rubric.md)
- **Example .research/IDEA.md files**: [references/examples/](references/examples/)
