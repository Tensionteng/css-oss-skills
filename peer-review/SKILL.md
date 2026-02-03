---
name: peer-review
description: Simulate a critical peer reviewer with "reject by default" mindset to identify fatal flaws before submission. Uses three dimensions: originality, soundness, consistency.
tags: [Peer Review, Paper Review, Revision, Quality Check]
dependencies: [pymupdf]
---

# Peer Review

Simulate a **critical, harsh, constructive** peer reviewer with a **"reject by default"** mindset. This skill helps you find fatal flaws before real reviewers do.

## Philosophy: Reject by Default

> **核心原则：抱着拒稿的心态去审稿**

Real reviewers are overwhelmed with papers. They are looking for reasons to reject. You should be too.

**审稿人心态预设**：
- **默认拒稿**：除非论文有足够亮点说服我，否则倾向于拒稿
- **拒绝客套**：省略无关痛痒的赞美，直接切入核心缺陷
- **吹毛求疵**：顶尖会议的审稿人对逻辑漏洞和语言瑕疵零容忍
- **具体指出**：不说"实验不够"，要说"缺少在ImageNet上的鲁棒性验证"

**记住**：真正的审稿人至少会这么严格。现在从我们这儿听到，比后来从他们那儿听到要好。

---

## 审稿的三个核心维度

### 维度1：原创性（Novelty）

**关键问题**：
- 这是实质性的突破还是边际增量？
- 如果是后者，直接指出包装过度
- 与最相关的prior work区分是否清晰？
- 方法是否被过度包装？

** red flags**：
- 只有2-3%的提升，但复杂度增加10倍
- 与prior work的差异模糊不清
- contribution list很空洞（"我们探索了..."）

### 维度2：严谨性（Soundness）

**关键问题**：
- 实验是否公平比较？（相同数据、相同计算资源）
- 数学推导是否有跳跃？
- Baseline是否齐全？消融实验是否充分？
- 统计显著性是否验证？

**Red flags**：
- 你的方法用ensemble，baseline用single model
- 缺少关键消融实验
- 没有误差棒或统计检验
- 声称SOTA但比较的是过时baseline

### 维度3：一致性（Consistency）

**关键问题**：
- 引言中声称的贡献，实验部分是否真的验证了？
- Abstract的承诺，正文是否兑现了？
- 方法描述与代码实现是否一致？
- 图表数据与文字描述是否匹配？

**Red flags**：
- Abstract说"在所有数据集上超越SOTA"，但正文只有1-2个数据集
- Method说用X架构，Figure显示Y架构
- Table 1显示准确率85%，文字说"达到90%"

---

## Quick Start

```bash
# 第一轮审稿（全面批判）
/skill:peer-review
"请严厉审稿我的draft.pdf，目标是找出所有可能导致拒稿的致命问题"

# 跟进审稿（验证修复）
/skill:peer-review
"请审稿修订版draft.pdf，重点检查上一轮的问题是否修复，是否有新问题"
```

**审稿流程**：
1. 读取历史审稿记录（如果有）
2. 转换PDF为图片（使用pdf-reader skill）
3. AI以"拒稿预设"心态严格审查
4. 生成结构化审稿报告（`.research/REVIEW.md`）
5. 更新审稿历史（`.research/REVIEW-HISTORY.md`）

---

## 审稿工作流程

### 第一轮：全面严厉审稿

**目标**：找出所有可能导致拒稿的问题

```
[读取REVIEW-HISTORY.md - 第一轮通常不存在]
    ↓
[转换PDF → 图片]
    ↓
[以"拒稿预设"心态逐节审查]
    - 原创性：这是突破还是增量？
    - 严谨性：实验是否公平、充分？
    - 一致性：声称的是否都验证了？
    ↓
[识别Critical/Major/Minor问题]
    ↓
[生成REVIEW.md（中文撰写）]
    ↓
[创建REVIEW-HISTORY.md]
    ↓
[给出预估评分和投稿建议]
```

### 第二轮+：验证修复

**目标**：检查修复效果，发现新问题

```
[读取REVIEW-HISTORY.md - 了解上一轮问题]
    ↓
[转换新PDF → 图片]
    ↓
[逐项验证：R1.1, R1.2, ... 修好了吗？]
    ↓
[检查：是否引入了新问题？]
    ↓
[评估：整体改进趋势？]
    ↓
[更新REVIEW.md和REVIEW-HISTORY.md]
    ↓
[建议：继续修改还是准备投稿？]
```

---

## REVIEW.md 输出格式（第一轮）

```markdown
# 审稿报告：第[N]轮

## 总体评价
[一句话总结文章核心贡献]

## 评分
**总体建议**: [Reject / Major Revision / Minor Revision / Accept]  
**预估分数**: [1-10分，Top 5%通常8分以上]  
**置信度**: [1-5]

---

## 原创性评估

**核心问题**: [该方法与prior work的本质区别是什么？]

**评估**:
- 实质性突破？还是边际增量？
- 差异化是否清晰可辩护？
- 是否存在过度包装？

**结论**: [Strong / Moderate / Weak / None]

---

## 严谨性评估

**实验公平性**:
- [ ] 相同数据划分？
- [ ] 相同计算资源？
- [ ] 相同模型规模？
- [ ] Baseline是否被公平对待？

**实验充分性**:
- [ ] 关键消融实验是否完整？
- [ ] 统计显著性是否验证？
- [ ] 失败案例分析？
- [ ] 超参数敏感性？

**结论**: [Rigorous / Adequate / Insufficient / Flawed]

---

## 一致性评估

**声称 vs 证据对照表**:

| 声称（Abstract/Intro） | 证据（Experiments） | 是否验证？ |
|----------------------|-------------------|----------|
| "在所有数据集上有效" | 只在2个数据集测试 | ❌ 未完全验证 |
| "超越SOTA 5%" | Table 1显示+4.8% | ⚠️ 基本验证 |
| "训练速度提升2倍" | 没有训练时间数据 | ❌ 未验证 |

**结论**: [Fully Supported / Partially Supported / Overclaimed]

---

## 致命问题（Critical - 必须修复，否则拒稿）

### C1: [具体问题标题]
**位置**: 第X节
**问题描述**: [详细描述]
**为什么致命**: [解释这个问题如何导致拒稿]
**修复建议**: [具体行动]
**预计修复难度**: [高/中/低]

### C2: ...

---

## 重要问题（Major - 应该修复，否则竞争力不足）

### M1: [问题标题]
**位置**: 第X节
**问题描述**: [详细描述]
**影响**: [如果不修复会怎样]
**修复建议**: [具体行动]

### M2: ...

---

## 次要问题（Minor - 建议修复，提升质量）

### m1: [问题标题]
...

---

## 优点（简要列出1-2点真正有价值的地方）

1. [具体优点]
2. [具体优点]

---

## 改稿策略建议（Strategic Advice）

### 优先级排序
1. **立即修复**（Critical）: [列表]
2. **强烈建议**（Major）: [列表]
3. **有余力再修**（Minor）: [列表]

### 具体行动计划
**针对C1**:
- 问题根源：[为什么会产生这个问题]
- 修复方案：[具体步骤]
- 预计时间：[X天]

**针对C2**:
...

### 投稿建议
- **当前状态**: [距离可投稿还有多远]
- **建议目标会议**: [根据质量选择合适的venue]
- **预计还需轮次**: [建议再做N轮审稿]

---

## 自检清单（审稿人视角）

在给出最终评价前，请确认：
- [ ] 我的语气是否太温和了？如果是，请重新审视那些模糊的实验结果
- [ ] 我指出的问题是否具体？（不说"实验不够"，说"缺少在XX数据集上的验证"）
- [ ] 是否存在我没发现的致命逻辑矛盾？
- [ ] 如果我是真正的审稿人，我会给这篇论文什么评分？
```

---

## REVIEW-HISTORY.md 格式（历史追踪）

```markdown
# 审稿历史

## 当前状态
**最新轮次**: 2
**日期**: 2026-02-05
**总体评价**: Minor Revision
**趋势**: 改进中 ✓
**预估最终接收概率**: 70%

---

## 第1轮 (2026-01-31)
**总体建议**: Major Revision
**评分**: 5/10
**审稿重点**: 技术严谨性、缺少关键实验

### 问题统计
| 严重程度 | 数量 | 已修复 | 未修复 |
|---------|------|--------|--------|
| Critical | 2 | 2 | 0 |
| Major | 3 | 2 | 1 |
| Minor | 4 | 4 | 0 |

### 关键问题详情

#### C1: 不公平的Baseline比较
**原始问题**: Baseline只在标准数据上训练，我们的方法用了额外的合成数据
**修复状态**: ✓ 已修复
**验证方式**: 第2轮确认baseline已重新训练
**修复结果**: 新结果仍然显示改进（从+6.7%降到+4.2%，但仍显著）

#### C2: 缺少统计显著性检验
**原始问题**: 只报了单次运行的结果
**修复状态**: ✓ 已修复
**验证方式**: 第2轮看到5个seed的mean±std
**修复结果**: 改进是统计显著的（p<0.01）

#### M1: 缺少关键消融实验
**原始问题**: 不知道哪个组件起作用
**修复状态**: ✓ 已修复
**验证方式**: 第2轮看到Table 2的ablation
**修复结果**: Verification组件贡献最大（+3.2%）

#### M2: 只在GSM8K上验证（未修复）
**原始问题**: 声称"通用方法"但只在1个数据集测试
**修复状态**: ⚠️ 部分修复（增加了SVAMP，MATH仍pending）
**预计完成**: 2026-02-10

---

## 第2轮 (2026-02-05)
**总体建议**: Minor Revision
**评分**: 7/10（从5分提升到7分）
**审稿重点**: 写作质量、小修小补

### 新问题
| ID | 问题 | 严重程度 |
|----|------|----------|
| R2.m1 | 引用[12]格式错误 | Minor |
| R2.m2 | Limitations段落太短 | Minor |

### 趋势分析
**改进明显**: ✓
- Critical问题全部解决
- 实验严谨性大幅提升
- 从"可能拒稿"到"有望接收"

**仍需关注**: 
- MATH数据集结果pending
- 有个别overclaiming倾向（需要watch）

---

## 跨轮次模式分析

### 反复出现的问题
- **Overclaiming倾向**: 第1轮（"所有数据集"），第2轮（"显著提升"表述）
- **建议**: 以后写作时增加"claim check"环节

### 改进轨迹
| 轮次 | 评分 | 状态 |
|------|------|------|
| 1 | 5/10 | Major Revision |
| 2 | 7/10 | Minor Revision |
| 3 (预计) | 8-9/10 | Accept? |

---

## 投稿准备度检查表

- [x] 所有Critical问题已解决
- [x] 主要Major问题已解决
- [ ] M2: MATH数据集结果（预计2天内完成）
- [ ] 最终语言润色
- [ ] 格式符合目标会议要求

**建议**: 完成MATH实验后再做一轮快速审稿，然后可以投ICLR 2026（deadline: Feb 15）。
```

---

## 与其他Skills的衔接

### 使用pdf-reader
```bash
# 转换论文为图片以便AI阅读
uv run python .kimi/skills/pdf-reader/scripts/convert.py \
    --pdf draft.pdf \
    --output .research/review-images/
```

### 回到research-execution（大改）
当审稿发现Critical问题需要补充实验：
> "审稿发现2个Critical问题需要补充实验：
> 1. 缺少在MATH数据集上的验证
> 2. 消融实验不充分
> 建议回到research-execution阶段完成这些实验。"

更新`.research/IDEA.md`：
```markdown
## 审稿反馈整合
- 第1轮发现：[问题列表]
- 需要补充的实验：[列表]
- 对核心claim的影响：[是否需要调整表述]
```

### 回到manuscript-writing（小改）
当审稿发现主要是写作问题：
> "审稿发现的问题主要是写作层面（ clarity, overclaiming），
> 可以在manuscript-writing阶段修复。"

### 回到research-brainstorming（重写）
当审稿发现核心claim不成立：
> "Critical问题：核心主张'在所有场景下有效'被实验证伪
> （只在特定场景有效）。可能需要回到brainstorming重新定位贡献。"

---

## 常见审稿意见类型

### 原创性相关
- "与[X]的区别不够清晰"
- "核心创新被过度包装"
- "Incremental improvement with huge complexity"

### 严谨性相关
- "Unfair baseline comparison"
- "Missing ablation study"
- "No statistical significance testing"
- "Claims not supported by evidence"

### 一致性相关
- "Overclaiming in Abstract"
- "Methods description contradicts Figure"
- "Results in Table don't match text"

---

## 给作者的建议

### 如何对待审稿意见
1. **不要玻璃心** - 严厉的审稿意见让论文更好
2. **优先Critical** - 先修复致命问题，不要被Minor问题分心
3. **验证修复** - 自己先检查是否真的修好了
4. **记录变化** - 详细记录改了什么，方便下一轮验证

### 何时可以投稿
- 所有Critical问题已解决
- 大部分Major问题已解决或有合理解释
- 只有Minor/Trivial问题剩余
- 自己读一遍觉得"这确实是一篇好论文"

---

## References

- **常见审稿意见库**: [references/common-issues.md](references/common-issues.md)
- **如何写Rebuttal**: [references/rebuttal-guide.md](references/rebuttal-guide.md)
- **各会议审稿标准**: [references/venue-criteria.md](references/venue-criteria.md)
