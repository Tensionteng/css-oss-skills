# 常见审稿意见库

审稿人最常用的批评类型，作为审稿时的检查清单。

---

## 致命问题（Critical）- 可能导致直接拒稿

### "Claim Not Supported by Evidence"
**典型表述**: "实验不支持作者声称的结论"
**怎么发现**:
- 检查Abstract/Intro的每句话是否都有实验支持
- Table 1的数据真的支持sentence 3的说法吗？
- "显著提升"真的显著吗？

**修复**:
- 软化claim到证据支持的范围
- 或者补充实验

### "Unfair Baseline"
**典型表述**: "Baseline比较不公平"
**常见形式**:
- 不同训练数据（你的方法用额外数据）
- 不同模型大小（你的用large，baseline用base）
- 不同计算预算（你训练10个epoch，baseline只训3个）
- 不同的evaluation metric
- 你的报best run，baseline报average

**修复**:
- 重新训练baseline，确保条件相同
- 或者明确说明并bound这个限制

### "Missing Critical Baseline"
**典型表述**: "缺少与[X]的比较，而这是该领域的SOTA"
**怎么发现**:
- 最近2年的相关工作是否都cited了？
- 有没有故意避开某个更强的方法？
- 有没有只和过时方法比较？

### "No Statistical Significance"
**典型表述**: "没有统计显著性检验"
**问题**: 85.2 vs 84.9可能只是噪声
**修复**:
- 跑5-10个random seeds
- 报mean ± std
- 做t-test

### "Method Not Clear / Not Reproducible"
**典型表述**: "方法描述不清晰，无法复现"
**怎么发现**:
- 给同事看，他能实现吗？
- 所有超参数都列了吗？
- 关键实现细节在正文还是appendix？

---

## 重要问题（Major）- 影响竞争力

### 原创性相关

### "Claim Not Supported by Evidence"
**What it means**: You said X but experiments don't show X
**How to catch it**:
- Check every sentence in Abstract/Intro against experiments
- Does Table 1 support the claim in sentence 3?
- Is the "significant improvement" actually significant?

**Fix**:
- Soften claim to what evidence supports
- Or run additional experiments

### "Unfair Baseline"
**What it means**: You're comparing apples to oranges
**Common forms**:
- Different training data
- Different model size
- Different compute budget
- Different evaluation metric
- Cherry-picked best run vs your average

**Fix**:
- Re-train baseline with same conditions
- Or clearly state limitations

### "No Statistical Significance"
**What it means**: 85.2 vs 84.9 might be noise
**How to catch it**:
- Error bars? Standard deviation?
- Multiple random seeds?
- p-values for comparisons?

**Fix**:
- Run multiple seeds (5+)
- Report mean ± std
- Do statistical test (t-test)

### "Method Not Clear"
**What it means**: Can't reproduce from description
**How to catch it**:
- Give paper to colleague, can they implement it?
- Are all hyperparameters specified?
- Is algorithm pseudocode complete?

**Fix**:
- Add details
- Release code
- Add appendix with full specs

## Novelty Issues

### "Incremental Improvement"
**What it means**: +0.5% with 10x complexity
**How to catch it**:
- Is improvement substantial?
- Is complexity justified?
- Would anyone actually use this?

**Fix**:
- Show where simpler methods fail
- Demonstrate efficiency gains
- Find qualitative differences

### "Not Novel"
**What it means**: Prior work already did this
**How to catch it**:
- Check citations carefully
- Is [27] essentially the same idea?
- Did [15] try this approach?

**Fix**:
- Clarify differences (be explicit!)
- Or acknowledge and extend
- Or pivot to different angle

### "Unclear Contribution"
**What it means**: What exactly is new?
**Common in**: Papers with vague claims ("we explore...")

**Fix**:
- Make contribution bullets specific
- "We propose X which achieves Y"
- Not: "We study the problem of Z"

## Completeness Issues

### "Missing Ablations"
**What it means**: Which component matters?
**Essential ablations**:
- Full model vs -component A
- Different architecture choices
- Sensitivity to hyperparameters

**Fix**:
- Add ablation table
- Show what matters and what doesn't

### "No Error Analysis"
**What it means**: When does it fail? Why?
**What to show**:
- Failure cases (categories)
- Comparison: where baseline fails vs where you fail
- Qualitative examples

**Fix**:
- Add error analysis section
- Show examples
- Categorize failures

### "No Limitations"
**What it means**: Paper pretends method is perfect
**How to catch it**:
- Is there a Limitations section?
- Does it acknowledge real weaknesses?
- Or is it just lip service?

**Fix**:
- Be honest about weaknesses
- Reviewers appreciate honesty
- Shows you understand your method

### "Narrow Scope"
**What it means**: Only works on one specific setting
**How to catch it**:
- Does it work on other datasets?
- Other domains?
- Other languages (for NLP)?

**Fix**:
- Test on more settings
- Or narrow claim scope
- Or acknowledge limitation

## Clarity Issues

### "Hard to Follow"
**What it means**: Narrative jumps around
**How to catch it**:
- Ask colleague to read intro
- Do they understand the problem?
- Can they explain your solution back?

**Fix**:
- Add more signposting ("In Section 3, we...")
- One idea per paragraph
- Clear transition sentences

### "Notation Inconsistent"
**What it means**: X means different things in different places
**How to catch it**:
- Search for all uses of X
- Do they match?
- Did you change notation mid-paper?

**Fix**:
- Make notation table
- Check consistency
- Use different symbols for different concepts

### "Figure Unclear"
**What it means**: Can't understand figure without text
**Good figure**:
- Stands alone (caption explains everything)
- Axes labeled
- Legend clear
- Readable font

**Fix**:
- Rewrite caption
- Make figure larger
- Add annotations

### "Missing Details in Appendix"
**What it means**: Important info relegated to supplementary material
**How to catch it**:
- Key hyperparameters in main paper?
- Important proofs accessible?
- Dataset details clear?

**Fix**:
- Move critical details to main paper
- Appendix for truly extra stuff only

## Presentation Issues

### "Typos / Grammar"
**What it means**: Distracting errors
**Common**:
- "recieve" (receive)
- "it's" vs "its"
- Missing articles (a/an/the)
- Subject-verb agreement

**Fix**:
- Spell check
- Grammar check
- Read aloud
- Native speaker review

### "Broken Citations"
**What it means**: [?] or wrong reference
**How to catch it**:
- Check all [numbers]
- Do they exist in references?
- Are numbers sequential?

**Fix**:
- Fix LaTeX
- Run BibTeX again
- Check for duplicates

### "Formatting Issues"
**What it means**: Doesn't follow template
**Common**:
- Wrong font size
- Margins wrong
- Figure placement bad
- Page limit exceeded

**Fix**:
- Check template carefully
- Use provided style files
- Don't modify .sty files

## Ethical / Rigor Issues

### "Dataset Leakage"
**What it means**: Test data in training
**How to catch it**:
- Any preprocessing on full dataset?
- Feature selection on train+test?
- Any overlap between splits?

**Fix**:
- Re-do with proper splits
- Be very careful about preprocessing

### "Cherry-Picked Results"
**What it means**: Showing best of many runs
**How to catch it**:
- Did you run multiple seeds?
- Report all or average?
- Any runs discarded?

**Fix**:
- Report mean ± std over multiple seeds
- Or clearly state if single run

### "Unreproducible"
**What it means**: Can't replicate results
**How to catch it**:
- Code available?
- Random seeds specified?
- Environment documented?

**Fix**:
- Release code
- Document everything
- Provide requirements.txt

## Quick Checklist by Section

### Title
- [ ] Accurate (not misleading)
- [ ] Specific (not "A Study of...")
- [ ] Interesting

### Abstract
- [ ] All claims supported by paper
- [ ] Concrete numbers (not vague "improves performance")
- [ ] Clear problem and solution

### Introduction
- [ ] Problem well-motivated
- [ ] Contributions specific and clear
- [ ] Roadmap of paper

### Related Work
- [ ] Key papers cited
- [ ] Differences explained
- [ ] Not just a list

### Method
- [ ] Reproducible from description
- [ ] All hyperparameters listed
- [ ] Pseudocode if algorithmic

### Experiments
- [ ] Strong baselines
- [ ] Fair comparison
- [ ] Multiple seeds
- [ ] Significance tests
- [ ] Ablations

### Results
- [ ] Main claim supported
- [ ] Error analysis
- [ ] Failure cases shown

### Conclusion
- [ ] Honest limitations
- [ ] Not overclaiming
- [ ] Future work realistic

### References
- [ ] All citations in text exist
- [ ] Recent work included
- [ ] Format correct
