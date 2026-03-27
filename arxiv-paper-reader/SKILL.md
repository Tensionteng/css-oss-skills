---
name: arxiv-paper-reader
description: 自动下载 arXiv 论文 LaTeX 源码，分析内容并生成中文 Markdown 阅读报告。支持批量处理、自动去重、图片提取和索引维护。
license: MIT
metadata:
  author: tengshiyuan
  tags: [ArXiv, Paper Reading, LaTeX, Literature Review, Chinese]
  dependencies: [requests>=2.28.0, pymupdf>=1.23.0]
---

# arXiv 论文阅读器

自动下载 arXiv 论文的 LaTeX 源码，提取关键内容并生成结构化中文阅读报告。当 LaTeX 不可用时自动降级到 PDF 分析模式。

## 快速开始

```bash
# 单篇论文分析
python scripts/arxiv_reader.py 2405.12345

# 批量处理多篇论文
python scripts/arxiv_reader.py 2405.12345 2403.45678 2401.99999

# 强制重新生成（覆盖已有报告）
python scripts/arxiv_reader.py 2405.12345 --force

# 输出到其他目录
python scripts/arxiv_reader.py 2405.12345 --output ./my-papers/
```

**输出位置**: `.arxiv-paper/` 目录（自动创建）

---

## 核心工作流程

### 单次分析流程

```
接收 arXiv ID → 检查是否已存在 → 下载 LaTeX 源码 → 
解析文档结构 → 提取关键图片 → 生成中文报告 → 更新索引
        ↓（无源码时）
    降级到 PDF 模式 → 提取关键页面 → 生成简化报告
```

### 报告结构

生成的 Markdown 报告包含以下章节（中文）：

| 章节 | 内容说明 |
|-----|---------|
| **标题** | 论文题目的中文翻译 |
| **论文概览** | 原始标题、作者、核心贡献 bullet points |
| **研究背景和动机** | 问题定义、相关工作、研究意义 |
| **方法** | 核心方法描述、架构图、关键公式 |
| **实验结果** | 主要结果表格、关键图表、与 baseline 对比 |
| **伪代码** | 算法流程的代码形式 |
| **总结** | 主要贡献总结、局限性、未来方向 |

---

## 使用指南

### 基本用法

**分析单篇论文：**
```bash
python scripts/arxiv_reader.py 2405.12345
```
- 自动下载 LaTeX 源码
- 生成报告到 `.arxiv-paper/2405.12345-Paper-Title.md`
- 图片保存到 `.arxiv-paper/2405.12345-Paper-Title/` 目录

**批量处理：**
```bash
python scripts/arxiv_reader.py 2405.12345 2403.45678 2401.99999
```
- 顺序处理每篇论文
- 自动跳过已存在的报告（除非使用 `--force`）
- 最后更新索引文件

### 命令行参数

```
python scripts/arxiv_reader.py [arxiv_ids...] [options]

参数:
  arxiv_ids          一个或多个 arXiv ID (如 2405.12345)

选项:
  --output DIR       输出目录 (默认: .arxiv-paper/)
  --force            强制重新生成，覆盖已有报告
  --pdf-only         仅使用 PDF 模式，不尝试下载 LaTeX
  --keep-temp        保留临时文件（用于调试）
  --verbose, -v      显示详细日志
```

### 重复检测机制

脚本会检查输出目录中是否已存在同名报告文件：

```bash
# 文件名格式: {arxiv_id}-{cleaned_paper_title}.md
# 例如: 2405.12345-Llama-2-Open-Foundation-and-Fine-Tuned-Chat-Models.md
```

如果检测到重复：
- 默认：跳过处理，提示用户已有报告路径
- `--force`：删除旧报告，重新生成

### 索引文件

`.arxiv-paper/README.md` 自动维护，格式：

```markdown
# arXiv 论文阅读报告索引

| arXiv ID | 原始标题 | 中文标题 | 分析日期 |
|---------|---------|---------|---------|
| 2405.12345 | Llama 2: Open Foundation... | Llama 2：开放基础模型... | 2026-03-27 |

## 快速链接
- [2405.12345-Llama-2...](./2405.12345-Llama-2-Open-Foundation...md)
```

---

## 工作原理

### LaTeX 源码处理

**下载和解压：**
- 通过 `https://arxiv.org/e-print/{id}` 下载源码压缩包
- 解压到临时目录进行处理

**内容提取（正则解析）：**
```python
# 提取标题
\\title\{([^}]+)\}

# 提取作者
\\author\{([^}]+)\}

# 提取摘要
\\begin\{abstract\}(.+?)\\end\{abstract\}

# 提取章节
\\section\{([^}]+)\}

# 递归处理 \input 和 \include
```

**图片处理：**
- 识别 LaTeX 目录中的图片文件（`.pdf`, `.png`, `.jpg`, `.eps`）
- PDF/EPS 图片转为 PNG 格式
- 按引用顺序命名：`figure_1.png`, `figure_2.png`...
- Markdown 中使用相对路径引用

### PDF 降级模式

当 LaTeX 源码不可用时：
1. 下载 PDF（`https://arxiv.org/pdf/{id}.pdf`）
2. 提取关键页面：
   - 第 1 页：标题、作者、摘要
   - 方法章节页（通过 AI 分析定位）
   - 实验章节页
3. 转换为 PNG 图片供 AI 分析
4. 生成简化版报告（内容基于 AI 图片分析）

---

## 与其他技能协作

### 与 research-brainstorming 结合
```bash
# 1. 先用 arxiv-paper-reader 分析相关论文
python scripts/arxiv_reader.py 2405.11111 2405.22222

# 2. 在 research-brainstorming 中引用
# "基于对 2405.11111 和 2405.22222 的分析..."
```

### 与 pdf-reader 结合
```bash
# 如果需要更深入的 PDF 分析
# pdf-reader 专注于视觉分析，arxiv-paper-reader 专注于结构化报告
```

---

## 常见问题

**问题：下载 LaTeX 源码失败**
```
Error: Failed to download LaTeX source (404)
```
- 原因：该论文未上传 LaTeX 源码，只有 PDF
- 解决：脚本会自动降级到 PDF 模式

**问题：图片显示不正确**
- 检查图片路径是否为相对路径 `./{folder}/figure_1.png`
- 确保图片成功转换为 PNG 格式
- EPS 格式图片可能需要额外工具（如 `pdftoppm`）

**问题：报告内容不完整**
- 某些非标准 LaTeX 结构可能无法解析
- 尝试使用 `--pdf-only` 强制 PDF 模式
- 或手动补充缺失内容

**问题：文件名太长**
- 脚本会自动截断超过 200 字符的文件名
- 保留 arXiv ID 确保唯一性

---

## 实现细节

**技术栈：**
- Python 3.8+
- `requests`: 下载 arXiv 文件
- `pymupdf`: PDF 处理和图片转换
- 正则表达式：LaTeX 解析

**支持的图片格式转换：**
| 源格式 | 目标格式 | 方法 |
|-------|---------|------|
| PDF | PNG | PyMuPDF |
| PNG/JPG | 保持原样 | 直接复制 |
| EPS | PNG | 可选（需 inkscape/pdftoppm）|

**性能参考：**
- 单篇论文处理时间：10-30 秒（LaTeX 模式）
- PDF 模式稍慢：20-60 秒（含页面渲染）
- 批量处理 10 篇论文：约 3-5 分钟

---

## 注意事项

1. **版权**：生成的报告仅供个人学习研究使用
2. **准确性**：AI 生成的中文翻译和总结可能不够精确，建议对照原文
3. **CS 术语**：专业名词（如 Transformer, Token, U-Net）保持英文原样
4. **图片质量**：复杂矢量图转换后可能略有损失

---

## 参考

- **实现细节**: [references/implementation.md](references/implementation.md)
- **LaTeX 解析策略**: [references/implementation.md#latex-parsing](references/implementation.md#latex-parsing)
- **错误排查**: [references/implementation.md#troubleshooting](references/implementation.md#troubleshooting)
