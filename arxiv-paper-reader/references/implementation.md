# arxiv-paper-reader 实现细节

本文档详细介绍 `arxiv-paper-reader` 的技术实现细节，供开发者参考。

---

## 架构概览

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   User Input    │────▶│  ArxivPaperReader │────▶│   LaTeX Mode    │
│  (arxiv IDs)    │     │    (main class)   │     │ (preferred)     │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                              │                           │
                              │ fallback                  │ download
                              ▼                           ▼
                       ┌──────────────┐          ┌─────────────────┐
                       │   PDF Mode   │◀─────────│ e-print tarball │
                       │  (fallback)  │          └─────────────────┘
                       └──────────────┘                  │
                                                          │ extract
                                                          ▼
                                                  ┌─────────────────┐
                                                  │   tex files     │
                                                  └─────────────────┘
                                                          │
                                                          │ parse
                                                          ▼
                                                  ┌─────────────────┐
                                                  │  LatexParser    │
                                                  └─────────────────┘
                                                          │
                                                          ▼
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   README.md     │◀────│  Update Index    │◀────│ Generate Report │
│   (index)       │     │                  │     │   (markdown)    │
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

---

## 模块说明

### 1. arxiv_reader.py

主脚本，负责协调整个流程。

#### 核心类：`ArxivPaperReader`

| 方法 | 职责 |
|-----|------|
| `download_latex_source()` | 从 `arxiv.org/e-print/{id}` 下载源码 |
| `download_pdf()` | 从 `arxiv.org/pdf/{id}.pdf` 下载 PDF |
| `extract_tex_files()` | 解压 tar.gz 归档，提取 .tex 文件 |
| `find_main_tex()` | 识别主文件（含 `\documentclass`）|
| `process_latex_mode()` | LaTeX 处理主流程 |
| `process_pdf_mode()` | PDF 降级处理流程 |
| `generate_markdown_report()` | 生成 Markdown 报告 |
| `update_index()` | 更新 README.md 索引 |

#### 下载策略

```python
# LaTeX 源码下载 URL
https://arxiv.org/e-print/{arxiv_id}

# PDF 下载 URL  
https://arxiv.org/pdf/{arxiv_id}.pdf

# 版本处理：arXiv 自动返回最新版本
# 如需指定版本：{arxiv_id}v1, {arxiv_id}v2, ...
```

### 2. latex_parser.py

LaTeX 解析模块，不依赖完整 LaTeX 编译器。

#### 核心类：`LatexParser`

| 方法 | 功能 |
|-----|------|
| `resolve_inputs()` | 递归解析 `\input` 和 `\include` |
| `extract_title()` | 提取标题 |
| `extract_authors()` | 提取作者信息 |
| `extract_abstract()` | 提取摘要 |
| `extract_sections()` | 提取章节结构 |
| `extract_figures()` | 提取图片环境 |
| `extract_tables()` | 提取表格环境 |
| `extract_algorithms()` | 提取算法伪代码 |
| `clean_latex_text()` | 清理 LaTeX 命令 |

#### 解析策略

**为什么不使用完整 LaTeX 编译器？**

1. **依赖太重**：需要安装 TeX Live/MiKTeX（数 GB）
2. **编译慢**：每次编译需要数秒到数分钟
3. **错误处理复杂**：编译错误难以自动恢复
4. **我们的需求**：只需提取内容，不需要精确排版

**正则解析的局限性：**

| 情况 | 处理方式 |
|-----|---------|
| 嵌套命令：`\textbf{\textit{text}}` | 递归清理 |
| 多行参数：`\title{...\n...}` | `re.DOTALL` 标志 |
| 转义字符：`\{`, `\}` | 特殊处理 |
| 条件编译：`\if...\fi` | 保留所有分支 |
| 自定义命令：`\newcommand` | 不展开，保留原样 |

---

## LaTeX 解析

### 输入解析

递归处理 `\input{file}` 和 `\include{file}`：

```python
def resolve_inputs(content, base_dir, depth=0):
    """递归展开所有输入文件。"""
    
    def replace_input(match):
        filename = match.group(1)
        # 尝试 .tex 扩展名
        for ext in ['.tex', '']:
            path = base_dir / (filename + ext)
            if path.exists():
                sub_content = read_file(path)
                # 递归处理
                sub_content = resolve_inputs(sub_content, path.parent, depth + 1)
                return f"\n% BEGIN {filename}\n{sub_content}\n% END {filename}\n"
        return f"% FILE NOT FOUND: {filename}"
    
    return re.sub(r'\\(?:input|include)\{([^}]+)\}', replace_input, content)
```

**防循环保护**：`max_depth=5` 防止循环引用导致栈溢出。

### 内容提取

#### 标题提取

```python
# 简单形式
\title{Paper Title}

# 带换行的复杂形式
\title{Multi-line
       Title}

# 正则模式
r'\\title\{([^}]*)\}'
```

#### 作者提取

支持多种形式：

```latex
% 简单形式
\author{Author Name}

% 带脚注
\author[1]{Author Name}
\affiliation[1]{Institution}

% 多作者
\author{Author1 \and Author2}

% 我们的解析器处理
authors = []
for match in re.finditer(r'\\author\{([^}]*)\}', content):
    # 分割 \and, \\, \thanks 等
    author_text = match.group(1)
```

#### 章节提取

```python
# 匹配所有章节级别
section_pattern = r'\\(section|subsection|subsubsection)\*?\{([^}]*)\}'

# 提取内容范围（到下一章节或文档结束）
for i, match in enumerate(matches):
    start = match.end()
    end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
    section_content = content[start:end]
```

---

## 图片处理

### 支持的图片格式

| 格式 | 处理方式 | 说明 |
|-----|---------|------|
| PDF | PyMuPDF 转 PNG | 学术论文中最常见 |
| PNG | 直接复制 | 保持不变 |
| JPG/JPEG | 直接复制 | 保持不变 |
| EPS | 外部工具转换 | 需要 pdftoppm 或 inkscape |

### PDF 转 PNG

```python
import fitz  # PyMuPDF

def convert_pdf_to_png(pdf_path, output_path, dpi=150):
    doc = fitz.open(str(pdf_path))
    page = doc[0]
    
    # 根据 DPI 计算缩放
    zoom = dpi / 72  # 72 is base DPI
    mat = fitz.Matrix(zoom, zoom)
    
    pix = page.get_pixmap(matrix=mat)
    pix.save(str(output_path))
    doc.close()
```

### EPS 转换（可选）

```bash
# 使用 pdftoppm (poppler-utils)
pdftoppm -png -r 150 input.eps output

# 或使用 inkscape
inkscape input.eps --export-filename=output.png --export-dpi=150
```

**注意**：如果系统没有这些工具，EPS 文件会被跳过。

---

## 报告生成

### 模板结构

```markdown
# {中文标题}

## 论文概览
- **原始标题**: {title}
- **作者**: {authors}
- **arXiv ID**: {arxiv_id}

### 核心贡献
<!-- AI 填充 -->

## 研究背景和动机
{abstract}
<!-- AI 扩展 -->

## 方法
<!-- AI 描述 -->
![图 1](./{folder}/figure_001.png)

## 实验结果
<!-- AI 总结 -->

## 伪代码
```python
# AI 提取
```

## 总结
<!-- AI 总结 -->
```

### 图片引用格式

```markdown
![图 1](./2405.12345-Paper-Title/figure_001.png)
```

**路径规则**：
- 相对路径：`./{folder_name}/{image_name}`
- 确保 Markdown 渲染时能正确找到图片

---

## 文件命名

### 清理规则

```python
def clean_filename(title, max_length=100):
    # 1. 替换特殊字符
    cleaned = re.sub(r'[\\/*?:"<>|]', '-', title)
    
    # 2. 空白变连字符
    cleaned = re.sub(r'\s+', '-', cleaned)
    
    # 3. 合并多个连字符
    cleaned = re.sub(r'-+', '-', cleaned)
    
    # 4. 修剪
    cleaned = cleaned.strip('-')
    
    # 5. 截断长度
    if len(cleaned) > max_length:
        cleaned = cleaned[:max_length].rsplit('-', 1)[0]
    
    return cleaned
```

### 完整文件名

```
{arxiv_id}-{cleaned_title}.md
```

**示例**：
- 输入：`Attention Is All You Need`
- arXiv ID：`1706.03762`
- 输出：`1706.03762-Attention-Is-All-You-Need.md`

---

## 索引文件

### 格式

```markdown
# arXiv 论文阅读报告索引

| arXiv ID | 标题 | 链接 |
|---------|------|------|
| 1706.03762 | Attention Is All You Need | [1706.03762-Attention...](./1706.03762-Attention...) |

---

*最后更新: 2026-03-27 12:00*
```

### 更新机制

每次处理完成后，扫描输出目录中的所有 `.md` 文件（排除 `README.md`），重新生成索引。

---

## 错误处理

### 常见错误

| 错误 | 原因 | 处理 |
|-----|------|------|
| 404 on e-print | 论文无 LaTeX 源码 | 降级到 PDF 模式 |
| 404 on PDF | arXiv ID 错误 | 报错退出 |
| 解压失败 | 损坏的压缩包 | 报错，尝试 PDF 模式 |
| 无 .tex 文件 | 非 LaTeX 项目 | 降级到 PDF 模式 |
| 图片转换失败 | 缺少依赖 | 跳过该图片，继续 |
| 文件名冲突 | 同名论文 | 保留 arXiv ID 区分 |

### 降级策略流程

```
开始处理
    │
    ▼
下载 LaTeX 源码
    │
    ├─► 成功 ──▶ 解压并解析 LaTeX ──▶ 提取图片 ──▶ 生成报告
    │
    └─► 失败 ──▶ 降级到 PDF 模式
                        │
                        ▼
                下载 PDF
                    │
                    ├─► 成功 ──▶ 提取关键页 ──▶ 生成简化报告
                    │
                    └─► 失败 ──▶ 报错退出
```

---

## 性能优化

### 下载优化

- 使用 `requests` 连接池
- 60 秒超时防止挂起
- 流式下载大文件

### 解析优化

- 正则预编译（在 `re.sub` 中自动处理）
- 只解析必要的结构
- 限制图片数量（默认最多 10 张）

### 内存优化

- 使用临时目录，自动清理
- 图片按需转换，不缓存
- `--keep-temp` 调试用

---

## 扩展开发

### 添加新的 LaTeX 命令支持

编辑 `latex_parser.py`：

```python
def extract_custom_element(self, content: str) -> List[Dict]:
    """Extract custom LaTeX environments."""
    pattern = r'\\begin\{customenv\}(.*?)\\end\{customenv\}'
    matches = []
    
    for match in re.finditer(pattern, content, re.DOTALL):
        matches.append({
            'content': self.clean_latex_text(match.group(1)),
            'raw': match.group(0)
        })
    
    return matches
```

### 添加新的图片格式支持

编辑 `arxiv_reader.py`：

```python
def convert_new_format(self, input_path: Path, output_path: Path) -> bool:
    """Convert new image format to PNG."""
    try:
        # 使用合适的库进行转换
        import some_library
        some_library.convert(input_path, output_path)
        return True
    except Exception as e:
        self.error(f"Conversion failed: {e}")
        return False
```

---

## Troubleshooting

### 调试模式

```bash
# 显示详细日志
python scripts/arxiv_reader.py 2405.12345 -v

# 保留临时文件
python scripts/arxiv_reader.py 2405.12345 -v --keep-temp
```

### 常见问题

**Q: 图片显示为红叉**
- 检查图片路径是否为相对路径
- 确认图片文件存在
- 检查 Markdown 渲染器是否支持相对路径

**Q: 报告内容为空**
- 检查 LaTeX 文件是否正确解析
- 使用 `-v` 查看解析日志
- 尝试 `--pdf-only` 强制 PDF 模式

**Q: 作者信息不准确**
- LaTeX 作者格式多样，解析可能不完整
- 建议手动核对作者信息

**Q: EPS 图片未转换**
- 安装 `poppler-utils` (Linux) 或 `inkscape`
- Ubuntu/Debian: `sudo apt-get install poppler-utils`
- macOS: `brew install poppler`
