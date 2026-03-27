#!/usr/bin/env python3
"""
ArXiv Paper Reader - Download and analyze arXiv papers, generate Chinese Markdown reports.

Usage:
    # Single paper
    python arxiv_reader.py 2405.12345
    
    # Multiple papers
    python arxiv_reader.py 2405.12345 2403.45678 2401.99999
    
    # Force regenerate
    python arxiv_reader.py 2405.12345 --force
"""

import argparse
import io
import os
import re
import shutil
import sys
import tarfile
import tempfile
from pathlib import Path
from typing import List, Optional, Tuple
from urllib.parse import urlparse

import requests

# Optional imports with fallbacks
try:
    import fitz  # PyMuPDF
    HAS_PYMUPDF = True
except ImportError:
    HAS_PYMUPDF = False
    print("Warning: pymupdf not installed. PDF conversion will be limited.")


class ArxivPaperReader:
    """Main class for reading and analyzing arXiv papers."""
    
    def __init__(self, output_dir: str = ".arxiv-paper", verbose: bool = False, keep_temp: bool = False):
        self.output_dir = Path(output_dir)
        self.verbose = verbose
        self.keep_temp = keep_temp
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def log(self, message: str):
        """Print log message if verbose mode."""
        if self.verbose:
            print(f"[INFO] {message}")
            
    def error(self, message: str):
        """Print error message."""
        print(f"[ERROR] {message}", file=sys.stderr)
        
    def download_latex_source(self, arxiv_id: str) -> Optional[bytes]:
        """Download LaTeX source from arXiv. Returns None if not available."""
        url = f"https://arxiv.org/e-print/{arxiv_id}"
        self.log(f"Downloading LaTeX source from {url}")
        
        try:
            response = requests.get(url, timeout=60)
            if response.status_code == 200:
                return response.content
            elif response.status_code == 404:
                self.log(f"LaTeX source not available for {arxiv_id}")
                return None
            else:
                self.error(f"Failed to download: HTTP {response.status_code}")
                return None
        except requests.RequestException as e:
            self.error(f"Network error: {e}")
            return None
    
    def download_pdf(self, arxiv_id: str) -> Optional[bytes]:
        """Download PDF from arXiv."""
        url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
        self.log(f"Downloading PDF from {url}")
        
        try:
            response = requests.get(url, timeout=60)
            if response.status_code == 200:
                return response.content
            else:
                self.error(f"Failed to download PDF: HTTP {response.status_code}")
                return None
        except requests.RequestException as e:
            self.error(f"Network error: {e}")
            return None
    
    def extract_tex_files(self, tar_data: bytes, temp_dir: Path) -> List[Path]:
        """Extract .tex files from tar.gz archive."""
        tex_files = []
        
        try:
            with tarfile.open(fileobj=io.BytesIO(tar_data), mode="r:gz") as tar:
                for member in tar.getmembers():
                    if member.name.endswith('.tex') and not member.name.startswith('__'):
                        tar.extract(member, temp_dir)
                        tex_files.append(temp_dir / member.name)
                        self.log(f"Extracted: {member.name}")
        except Exception as e:
            self.error(f"Failed to extract archive: {e}")
            
        return tex_files
    
    def find_main_tex(self, tex_files: List[Path]) -> Optional[Path]:
        r"""Find the main .tex file (usually contains \documentclass)."""
        for tex_file in tex_files:
            try:
                content = tex_file.read_text(encoding='utf-8', errors='ignore')
                if '\\documentclass' in content:
                    self.log(f"Found main tex file: {tex_file.name}")
                    return tex_file
            except Exception:
                continue
        
        # Fallback: return the first .tex file
        if tex_files:
            return tex_files[0]
        return None
    
    def clean_filename(self, title: str, max_length: int = 100) -> str:
        """Clean title for use in filename."""
        # Remove special characters
        cleaned = re.sub(r'[\\/*?:"<>|]', '-', title)
        # Replace whitespace with single hyphen
        cleaned = re.sub(r'\s+', '-', cleaned)
        # Remove multiple consecutive hyphens
        cleaned = re.sub(r'-+', '-', cleaned)
        # Trim
        cleaned = cleaned.strip('-')
        # Limit length
        if len(cleaned) > max_length:
            cleaned = cleaned[:max_length].rsplit('-', 1)[0]
        return cleaned
    
    def get_report_filename(self, arxiv_id: str, title: str) -> Tuple[str, str]:
        """Generate report filename and folder name."""
        cleaned_title = self.clean_filename(title)
        base_name = f"{arxiv_id}-{cleaned_title}"
        md_filename = f"{base_name}.md"
        folder_name = base_name
        return md_filename, folder_name
    
    def check_existing_report(self, arxiv_id: str, title: str) -> Optional[Path]:
        """Check if report already exists. Returns path if exists, None otherwise."""
        md_filename, _ = self.get_report_filename(arxiv_id, title)
        report_path = self.output_dir / md_filename
        
        if report_path.exists():
            return report_path
        
        # Also check by arxiv_id pattern
        for file in self.output_dir.glob(f"{arxiv_id}-*.md"):
            return file
            
        return None
    
    def convert_pdf_to_png(self, pdf_path: Path, output_path: Path, dpi: int = 150) -> bool:
        """Convert PDF image to PNG."""
        if not HAS_PYMUPDF:
            self.error("PyMuPDF not available, cannot convert PDF images")
            return False
            
        try:
            doc = fitz.open(str(pdf_path))
            page = doc[0]
            
            # Calculate zoom based on DPI
            zoom = dpi / 72
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            
            pix.save(str(output_path))
            doc.close()
            self.log(f"Converted {pdf_path.name} -> {output_path.name}")
            return True
        except Exception as e:
            self.error(f"Failed to convert PDF image: {e}")
            return False
    
    def extract_images_from_latex(self, tex_dir: Path, output_dir: Path) -> List[Path]:
        """Extract and convert images from LaTeX source."""
        image_files = []
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Common image extensions in LaTeX
        extensions = ['.pdf', '.png', '.jpg', '.jpeg', '.eps']
        
        for ext in extensions:
            for img_path in tex_dir.rglob(f"*{ext}"):
                if img_path.is_file():
                    if ext == '.pdf':
                        # Convert PDF to PNG
                        output_name = f"figure_{len(image_files)+1:03d}.png"
                        output_path = output_dir / output_name
                        if self.convert_pdf_to_png(img_path, output_path):
                            image_files.append(output_path)
                    elif ext in ['.png', '.jpg', '.jpeg']:
                        # Copy as-is
                        output_name = f"figure_{len(image_files)+1:03d}{ext}"
                        output_path = output_dir / output_name
                        shutil.copy2(img_path, output_path)
                        image_files.append(output_path)
                        self.log(f"Copied {img_path.name} -> {output_name}")
                    elif ext == '.eps':
                        # Try to convert EPS (requires external tools)
                        output_name = f"figure_{len(image_files)+1:03d}.png"
                        output_path = output_dir / output_name
                        if self.convert_eps_to_png(img_path, output_path):
                            image_files.append(output_path)
        
        return image_files
    
    def convert_eps_to_png(self, eps_path: Path, output_path: Path) -> bool:
        """Convert EPS to PNG using available tools."""
        # Try pdftoppm first
        import subprocess
        
        try:
            # Convert EPS to PDF first (if possible), then to PNG
            result = subprocess.run(
                ['pdftoppm', '-png', '-r', '150', str(eps_path), str(output_path.with_suffix(''))],
                capture_output=True,
                timeout=30
            )
            if result.returncode == 0:
                # pdftoppm adds -1 suffix
                generated = output_path.with_name(output_path.stem + '-1.png')
                if generated.exists():
                    generated.rename(output_path)
                    self.log(f"Converted {eps_path.name} -> {output_path.name}")
                    return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        # Try inkscape
        try:
            result = subprocess.run(
                ['inkscape', str(eps_path), '--export-filename', str(output_path), '--export-dpi', '150'],
                capture_output=True,
                timeout=30
            )
            if result.returncode == 0:
                self.log(f"Converted {eps_path.name} -> {output_path.name}")
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        self.error(f"Could not convert EPS file {eps_path.name} (pdftoppm/inkscape not available)")
        return False
    
    def parse_latex_content(self, tex_content: str) -> dict:
        """Parse LaTeX content to extract paper structure."""
        result = {
            'title': '',
            'authors': '',
            'abstract': '',
            'sections': [],
            'figures': [],
            'algorithms': []
        }
        
        # Extract title
        title_match = re.search(r'\\title\{([^}]+)\}', tex_content, re.DOTALL)
        if title_match:
            result['title'] = self.clean_latex_commands(title_match.group(1))
        
        # Extract authors
        author_match = re.search(r'\\author\{([^}]+)\}', tex_content, re.DOTALL)
        if author_match:
            result['authors'] = self.clean_latex_commands(author_match.group(1))
        
        # Extract abstract
        abstract_match = re.search(r'\\begin\{abstract\}(.+?)\\end\{abstract\}', tex_content, re.DOTALL | re.IGNORECASE)
        if abstract_match:
            result['abstract'] = self.clean_latex_commands(abstract_match.group(1))
        
        # Extract sections
        section_pattern = r'\\section\{([^}]+)\}'
        sections = re.findall(section_pattern, tex_content)
        result['sections'] = [self.clean_latex_commands(s) for s in sections]
        
        return result
    
    def clean_latex_commands(self, text: str) -> str:
        """Remove common LaTeX commands from text."""
        # Remove comments
        text = re.sub(r'(?<!\\)%.*?\n', '\n', text)
        # Remove common commands
        text = re.sub(r'\\[a-zA-Z]+\*?(\{[^}]*\})*', ' ', text)
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def resolve_latex_inputs(self, main_tex: Path) -> str:
        r"""Resolve \input and \include commands in LaTeX."""
        base_dir = main_tex.parent
        
        def replace_input(match):
            filename = match.group(1)
            # Try with and without .tex extension
            for ext in ['.tex', '']:
                input_path = base_dir / (filename + ext)
                if input_path.exists():
                    try:
                        content = input_path.read_text(encoding='utf-8', errors='ignore')
                        return f"\n% BEGIN {filename}\n{content}\n% END {filename}\n"
                    except Exception:
                        break
            return f"% Could not include: {filename}"
        
        try:
            content = main_tex.read_text(encoding='utf-8', errors='ignore')
            # Replace \input and \include
            content = re.sub(r'\\(?:input|include)\{([^}]+)\}', replace_input, content)
            return content
        except Exception as e:
            self.error(f"Failed to read main tex: {e}")
            return ""
    
    def generate_markdown_report(self, arxiv_id: str, paper_info: dict, image_files: List[Path], 
                                 folder_name: str) -> str:
        """Generate Chinese Markdown report."""
        
        # Generate relative image paths
        image_refs = []
        for i, img_path in enumerate(image_files[:10], 1):  # Limit to 10 images
            rel_path = f"./{folder_name}/{img_path.name}"
            image_refs.append(f"![图 {i}]({rel_path})")
        
        # Create markdown content
        md_content = f"""# {paper_info.get('title_zh', paper_info.get('title', 'Unknown Title'))}

## 论文概览

- **原始标题**: {paper_info.get('title', 'N/A')}
- **作者**: {paper_info.get('authors', 'N/A')}
- **arXiv ID**: {arxiv_id}
- **分析日期**: {__import__('datetime').datetime.now().strftime('%Y-%m-%d')}

### 核心贡献

<!-- AI should extract key contributions here -->
- 
- 
- 

## 研究背景和动机

{paper_info.get('abstract', '待补充：请基于摘要和引言部分填写')}

<!-- AI should expand on background based on introduction -->

## 方法

<!-- AI should describe the method based on the paper content -->

### 关键图表

"""
        # Add up to 5 most important figures
        for i, img_ref in enumerate(image_refs[:5], 1):
            md_content += f"\n**图 {i}**: {img_ref}\n\n"
        
        md_content += """
## 实验结果

<!-- AI should summarize key experimental results -->

### 主要结果

| 指标 | 数值 | 备注 |
|-----|------|------|
| - | - | 待补充 |

### 关键图表

"""
        # Add remaining figures
        for i, img_ref in enumerate(image_refs[5:], 6):
            md_content += f"\n**图 {i}**: {img_ref}\n\n"
        
        md_content += """
## 伪代码

<!-- AI should extract or reconstruct pseudocode from the paper -->

```python
# 待补充：从论文中提取算法伪代码
```

## 总结

### 主要贡献

<!-- AI should summarize main contributions -->

### 局限性

<!-- AI should note any limitations mentioned or observed -->

### 未来方向

<!-- AI should suggest future research directions -->

---

*本报告由 arxiv-paper-reader 自动生成，内容需要 AI 进一步填充完善。*
"""
        
        return md_content
    
    def process_latex_mode(self, arxiv_id: str, force: bool = False) -> Optional[Path]:
        """Process paper in LaTeX mode. Returns path to generated report."""
        print(f"\n{'='*60}")
        print(f"Processing {arxiv_id} (LaTeX mode)")
        print(f"{'='*60}")
        
        # Download LaTeX source
        latex_data = self.download_latex_source(arxiv_id)
        if latex_data is None:
            self.log("LaTeX source not available, falling back to PDF mode")
            return None
        
        # Create temp directory
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Extract tex files
            tex_files = self.extract_tex_files(latex_data, temp_path)
            if not tex_files:
                self.error("No .tex files found in archive")
                return None
            
            # Find main tex file
            main_tex = self.find_main_tex(tex_files)
            if not main_tex:
                self.error("Could not identify main tex file")
                return None
            
            # Resolve inputs and parse content
            full_content = self.resolve_latex_inputs(main_tex)
            paper_info = self.parse_latex_content(full_content)
            
            if not paper_info['title']:
                paper_info['title'] = f"Unknown-Title-{arxiv_id}"
            
            # Check for existing report
            existing = self.check_existing_report(arxiv_id, paper_info['title'])
            if existing and not force:
                print(f"Report already exists: {existing}")
                return existing
            
            # Get output filenames
            md_filename, folder_name = self.get_report_filename(arxiv_id, paper_info['title'])
            report_path = self.output_dir / md_filename
            assets_dir = self.output_dir / folder_name
            
            # Extract and convert images
            tex_dir = main_tex.parent
            image_files = self.extract_images_from_latex(tex_dir, assets_dir)
            
            # Generate report
            md_content = self.generate_markdown_report(arxiv_id, paper_info, image_files, folder_name)
            report_path.write_text(md_content, encoding='utf-8')
            
            print(f"✓ Generated report: {report_path}")
            print(f"✓ Extracted {len(image_files)} images to: {assets_dir}")
            
            return report_path
    
    def process_pdf_mode(self, arxiv_id: str, force: bool = False) -> Optional[Path]:
        """Process paper in PDF mode (fallback). Returns path to generated report."""
        print(f"\n{'='*60}")
        print(f"Processing {arxiv_id} (PDF mode)")
        print(f"{'='*60}")
        
        if not HAS_PYMUPDF:
            self.error("PyMuPDF required for PDF mode")
            return None
        
        # Download PDF
        pdf_data = self.download_pdf(arxiv_id)
        if pdf_data is None:
            self.error("Failed to download PDF")
            return None
        
        # Create temp file for PDF
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_pdf:
            tmp_pdf.write(pdf_data)
            pdf_path = Path(tmp_pdf.name)
        
        try:
            # Open PDF with PyMuPDF
            doc = fitz.open(str(pdf_path))
            
            # Extract title from first page text
            first_page = doc[0]
            text = first_page.get_text()
            
            # Try to extract title (usually first line)
            lines = [l.strip() for l in text.split('\n') if l.strip()]
            title = lines[0] if lines else f"Unknown-Title-{arxiv_id}"
            
            # Check for existing report
            existing = self.check_existing_report(arxiv_id, title)
            if existing and not force:
                print(f"Report already exists: {existing}")
                doc.close()
                return existing
            
            # Get output filenames
            md_filename, folder_name = self.get_report_filename(arxiv_id, title)
            report_path = self.output_dir / md_filename
            assets_dir = self.output_dir / folder_name
            assets_dir.mkdir(parents=True, exist_ok=True)
            
            # Extract key pages as images
            image_files = []
            pages_to_extract = [0]  # First page always
            
            # Try to find method and experiment sections
            for i, page in enumerate(doc):
                page_text = page.get_text().lower()
                if any(kw in page_text for kw in ['method', 'approach', 'methodology', 'model']):
                    if i not in pages_to_extract:
                        pages_to_extract.append(i)
                elif any(kw in page_text for kw in ['experiment', 'result', 'evaluation', 'benchmark']):
                    if i not in pages_to_extract:
                        pages_to_extract.append(i)
                
                if len(pages_to_extract) >= 5:  # Limit pages
                    break
            
            # Convert pages to images
            for idx, page_num in enumerate(pages_to_extract, 1):
                page = doc[page_num]
                mat = fitz.Matrix(2, 2)  # 2x zoom for better quality
                pix = page.get_pixmap(matrix=mat)
                img_path = assets_dir / f"page_{idx:03d}.png"
                pix.save(str(img_path))
                image_files.append(img_path)
                self.log(f"Extracted page {page_num + 1} -> {img_path.name}")
            
            doc.close()
            
            # Generate simplified report
            paper_info = {
                'title': title,
                'title_zh': title,  # AI will translate
                'authors': 'See PDF',  # Could be extracted with more effort
                'abstract': 'See page_001.png'
            }
            
            md_content = self.generate_markdown_report(arxiv_id, paper_info, image_files, folder_name)
            # Add note about PDF mode
            md_content = md_content.replace(
                '*本报告由 arxiv-paper-reader 自动生成',
                '*本报告由 arxiv-paper-reader 自动生成（PDF模式，LaTeX源码不可用）'
            )
            report_path.write_text(md_content, encoding='utf-8')
            
            print(f"✓ Generated report (PDF mode): {report_path}")
            print(f"✓ Extracted {len(image_files)} pages to: {assets_dir}")
            
            return report_path
            
        finally:
            # Clean up temp PDF
            if pdf_path.exists():
                pdf_path.unlink()
    
    def update_index(self, reports: List[Path]):
        """Update the README.md index file."""
        index_path = self.output_dir / "README.md"
        
        # Collect report info
        entries = []
        for report_path in reports:
            if report_path and report_path.exists():
                # Parse arxiv_id and title from filename
                match = re.match(r'(.+?)-(.+)\.md$', report_path.name)
                if match:
                    arxiv_id = match.group(1)
                    title = match.group(2).replace('-', ' ')
                    entries.append({
                        'arxiv_id': arxiv_id,
                        'title': title,
                        'path': report_path.name
                    })
        
        # Generate index content
        lines = [
            "# arXiv 论文阅读报告索引",
            "",
            "| arXiv ID | 标题 | 链接 |",
            "|---------|------|------|"
        ]
        
        for entry in entries:
            lines.append(f"| {entry['arxiv_id']} | {entry['title']} | [{entry['path']}](./{entry['path']}) |")
        
        lines.extend([
            "",
            "---",
            "",
            f"*最后更新: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}*"
        ])
        
        index_path.write_text('\n'.join(lines), encoding='utf-8')
        print(f"\n✓ Updated index: {index_path}")
    
    def process(self, arxiv_ids: List[str], force: bool = False, pdf_only: bool = False):
        """Process one or more arXiv papers."""
        reports = []
        
        for arxiv_id in arxiv_ids:
            # Clean arxiv_id
            arxiv_id = arxiv_id.strip()
            
            # Remove URL prefix if present
            if 'arxiv.org' in arxiv_id:
                parsed = urlparse(arxiv_id)
                arxiv_id = parsed.path.strip('/').split('/')[-1]
            
            print(f"\nProcessing: {arxiv_id}")
            
            report_path = None
            
            # Try LaTeX mode first (unless pdf_only)
            if not pdf_only:
                try:
                    report_path = self.process_latex_mode(arxiv_id, force)
                except Exception as e:
                    self.error(f"LaTeX mode failed: {e}")
                    report_path = None
            
            # Fallback to PDF mode
            if report_path is None:
                try:
                    report_path = self.process_pdf_mode(arxiv_id, force)
                except Exception as e:
                    self.error(f"PDF mode failed: {e}")
            
            if report_path:
                reports.append(report_path)
        
        # Update index
        if reports:
            self.update_index(reports)
        
        print(f"\n{'='*60}")
        print(f"Completed: {len(reports)}/{len(arxiv_ids)} papers processed")
        print(f"Output directory: {self.output_dir.absolute()}")
        print(f"{'='*60}")


def main():
    parser = argparse.ArgumentParser(
        description="Download and analyze arXiv papers, generate Chinese Markdown reports"
    )
    
    parser.add_argument(
        'arxiv_ids',
        nargs='+',
        help='One or more arXiv IDs (e.g., 2405.12345) or URLs'
    )
    
    parser.add_argument(
        '--output', '-o',
        default='.arxiv-paper',
        help='Output directory (default: .arxiv-paper/)'
    )
    
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force regenerate, overwrite existing reports'
    )
    
    parser.add_argument(
        '--pdf-only',
        action='store_true',
        help='Only use PDF mode, do not attempt LaTeX download'
    )
    
    parser.add_argument(
        '--keep-temp',
        action='store_true',
        help='Keep temporary files (for debugging)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show verbose output'
    )
    
    args = parser.parse_args()
    
    reader = ArxivPaperReader(
        output_dir=args.output,
        verbose=args.verbose,
        keep_temp=args.keep_temp
    )
    
    reader.process(
        arxiv_ids=args.arxiv_ids,
        force=args.force,
        pdf_only=args.pdf_only
    )


if __name__ == "__main__":
    main()
