# AI Research Writing Skills

面向 AI/ML 研究的完整写作技能库，覆盖从想法到投稿的全过程。

## 核心设计：记忆系统

本套 skills 的核心设计是 **".research/ 共享画布"** —— 人和 AI 共用一组结构化文件来保持认知同步。

### 为什么需要记忆系统？

研究是**长周期、多轮次**的活动：
- 今天头脑风暴的想法，两周后写论文时需要回顾
- 第一轮审稿发现的问题，第三轮审稿时要检查是否修复
- 实验过程中发现的新现象，可能需要调整最初的研究角度

**没有记忆系统** = 每次对话都要重新交代背景，AI 遗忘，人疲惫。

### 记忆文件（.research/ 目录）

所有研究过程记录统一存放在 `.research/`，**全部用中文撰写**（方便人阅读）：

| 文件 | 内容 | 由谁更新 |
|------|------|---------|
| `IDEA.md` | 研究想法、头脑风暴记录、可行性评估 | research-brainstorming |
| `EXPERIMENT.md` | 实验计划、试点结果、分析决策 | research-execution |
| `REVIEW.md` | 当前轮次的审稿意见 | peer-review |
| `REVIEW-HISTORY.md` | 跨轮次的问题追踪、改进趋势 | peer-review |

### 论文草稿（paper-draft/）

最终的 LaTeX 论文放在项目根目录的 `paper-draft/`，**英文正文 + 中文注释**：

```latex
% 【中文注释】本文提出了一种自我验证机制...
We propose a self-verification mechanism...

% 【中文注释】现有方法的问题是...
Existing methods suffer from...
```

这样作者可以：
- **直接读中文**理解这段在讲什么
- **快速判断**英文表达是否准确
- **论文本身仍是纯英文**（注释不会出现在 PDF 中）

### 完整文件结构

```
your-project/
├── .research/              # 研究过程记录（中文，共享画布）
│   ├── IDEA.md            # 头脑风暴 → 可行角度
│   ├── EXPERIMENT.md      # 实验设计 → 结果分析
│   ├── REVIEW.md          # 当前审稿意见
│   └── REVIEW-HISTORY.md  # 审稿历史追踪
│
├── paper-draft/           # 论文正文（英文+中文注释）
│   ├── main.tex
│   ├── method.tex
│   └── ...
│
└── src/                   # 你的代码
```

### Skills 与记忆系统的交互

| 阶段 | Skill | 功能 | 读取 | 写入 |
|------|-------|------|------|------|
| 头脑风暴 | `research-brainstorming` | 讨论研究想法，确定可行角度 | - | `IDEA.md` |
| 实验执行 | `research-execution` | 设计渐进式实验，分析 baseline | `IDEA.md` | `EXPERIMENT.md` |
| PDF 阅读 | `pdf-reader` | 将论文 PDF 转为图片供 AI 分析 | - | `papers/` |
| 论文写作 | `manuscript-writing` | 分章节写作，中英文对照注释 | `EXPERIMENT.md` | `paper-draft/*.tex` |
| 审稿反馈 | `peer-review` | 模拟严厉审稿人，发现潜在问题 | `paper-draft/*.tex` | `REVIEW.md`, `REVIEW-HISTORY.md` |

### 使用示例

```bash
# 第 1 天：头脑风暴
/skill:research-brainstorming
"我想做 LLM 推理的研究"
# → AI 更新 .research/IDEA.md

# 第 3 天：设计实验
/skill:research-execution
"设计实验验证 IDEA.md 中的角度"
# → AI 读取 IDEA.md，更新 .research/EXPERIMENT.md

# 第 7 天：写论文
/skill:manuscript-writing
"写 Method 部分"
# → AI 读取 EXPERIMENT.md，生成 paper-draft/method.tex

# 第 10 天：审稿
/skill:peer-review
"审稿我的论文"
# → AI 读取 paper-draft/*.tex，更新 .research/REVIEW.md
```

模型会自动读取相关记忆文件，保持上下文连贯。

---

## 安装

所有安装方式都会**交互式询问**你选择全局安装（所有项目可用）或项目级安装（仅当前项目可用）。

### 方式一：npx（需 Node.js）

```bash
npx github:Tensionteng/css-oss-skills
```

---

### 方式二：curl/wget（无需 Node.js）

**Linux / macOS：**

```bash
curl -fsSL https://raw.githubusercontent.com/Tensionteng/css-oss-skills/main/install-local.sh | bash

# 如果没有curl，可以用wget：
wget -qO- https://raw.githubusercontent.com/Tensionteng/css-oss-skills/main/install-local.sh | bash
```

**Windows（PowerShell）：**

```powershell
iwr -useb https://raw.githubusercontent.com/Tensionteng/css-oss-skills/main/install-local.ps1 | iex
```

---

### 方式三：手动克隆

```bash
git clone https://github.com/Tensionteng/css-oss-skills.git
cd css-oss-skills
node bin/install.js
```

## 卸载

```bash
npx github:Tensionteng/css-oss-skills uninstall
```


**手动删除**（如需单独删除）：
```bash
# 全局安装位置
rm -rf ~/.claude/skills/*

# 项目级安装位置  
rm -rf .agents/
```

## 使用

```bash
# 头脑风暴
/skill:research-brainstorming
"我想做关于 LLM 推理的研究"

# 实验设计
/skill:research-execution
"设计实验验证这个想法"

# 写论文
/skill:manuscript-writing
"写一篇投 NeurIPS 的论文"

# 审稿
/skill:peer-review
"请审稿我的论文"
```
