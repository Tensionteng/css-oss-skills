#!/usr/bin/env python3
"""
LaTeX Parser - Helper module for parsing LaTeX source files.

Provides functions to extract structured content from LaTeX documents
without requiring a full LaTeX compiler.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class LatexParser:
    """Parser for LaTeX documents."""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        
    def log(self, message: str):
        """Print log message if verbose mode."""
        if self.verbose:
            print(f"[LATEX] {message}")
    
    def read_tex_file(self, filepath: Path) -> str:
        """Read a .tex file with proper encoding handling."""
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        
        for encoding in encodings:
            try:
                return filepath.read_text(encoding=encoding)
            except UnicodeDecodeError:
                continue
        
        # Last resort: read with errors ignored
        return filepath.read_text(encoding='utf-8', errors='ignore')
    
    def resolve_inputs(self, content: str, base_dir: Path, depth: int = 0, max_depth: int = 5) -> str:
        r"""
        Recursively resolve \input and \include commands.
        
        Args:
            content: LaTeX content
            base_dir: Directory to look for input files
            depth: Current recursion depth
            max_depth: Maximum recursion depth to prevent infinite loops
        
        Returns:
            Resolved content with all inputs expanded
        """
        if depth >= max_depth:
            return content
        
        def replace_input(match):
            command = match.group(0)
            filename = match.group(1)
            
            # Try with and without .tex extension
            for ext in ['.tex', '']:
                input_path = base_dir / (filename + ext)
                if input_path.exists():
                    try:
                        sub_content = self.read_tex_file(input_path)
                        # Recursively resolve inputs in the sub-content
                        sub_content = self.resolve_inputs(sub_content, input_path.parent, depth + 1, max_depth)
                        return f"\n% BEGIN INPUT: {filename}\n{sub_content}\n% END INPUT: {filename}\n"
                    except Exception as e:
                        return f"% ERROR including {filename}: {e}"
            
            return f"% FILE NOT FOUND: {filename}"
        
        # Match \input{file} and \include{file}
        pattern = r'\\(?:input|include)\{([^}]+)\}'
        return re.sub(pattern, replace_input, content)
    
    def extract_documentclass(self, content: str) -> Optional[Dict[str, str]]:
        """Extract document class and options."""
        pattern = r'\\documentclass\[(.*?)\]\{(.*?)\}'
        match = re.search(pattern, content)
        
        if match:
            return {
                'options': match.group(1).split(',') if match.group(1) else [],
                'class': match.group(2)
            }
        
        # Try without options
        pattern = r'\\documentclass\{(.*?)\}'
        match = re.search(pattern, content)
        if match:
            return {'options': [], 'class': match.group(1)}
        
        return None
    
    def extract_title(self, content: str) -> str:
        """Extract document title."""
        # Try \title{...}
        pattern = r'\\title\{([^}]*)\}'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            return self.clean_latex_text(match.group(1))
        
        return ""
    
    def extract_authors(self, content: str) -> List[Dict[str, str]]:
        """
        Extract author information.
        Returns list of dicts with 'name', 'affiliation', 'email'.
        """
        authors = []
        
        # Pattern for \author{name}
        author_pattern = r'\\author\{([^}]*)\}'
        
        # Pattern for \author[name]{affiliation}
        author_opt_pattern = r'\\author\[(.*?)\]\{(.*?)\}'
        
        # Try the optional pattern first
        for match in re.finditer(author_opt_pattern, content, re.DOTALL):
            authors.append({
                'name': self.clean_latex_text(match.group(1)),
                'affiliation': self.clean_latex_text(match.group(2)),
                'email': ''
            })
        
        # Fall back to simple pattern
        if not authors:
            for match in re.finditer(author_pattern, content, re.DOTALL):
                author_text = match.group(1)
                # Try to separate name and affiliation
                lines = [l.strip() for l in author_text.split('\\') if l.strip()]
                if lines:
                    authors.append({
                        'name': self.clean_latex_text(lines[0]),
                        'affiliation': self.clean_latex_text(' '.join(lines[1:])),
                        'email': ''
                    })
        
        return authors
    
    def extract_abstract(self, content: str) -> str:
        """Extract abstract content."""
        # Pattern for \begin{abstract}...\end{abstract}
        pattern = r'\\begin\{abstract\}(.*?)\\end\{abstract\}'
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        
        if match:
            return self.clean_latex_text(match.group(1))
        
        return ""
    
    def extract_sections(self, content: str) -> List[Dict[str, any]]:
        """
        Extract all sections with their content.
        Returns list of dicts with 'title', 'level', 'content'.
        """
        sections = []
        
        # Pattern for sections (section, subsection, subsubsection)
        pattern = r'\\(section|subsection|subsubsection)\*?\{([^}]*)\}'
        
        matches = list(re.finditer(pattern, content, re.DOTALL))
        
        for i, match in enumerate(matches):
            level = match.group(1)
            title = self.clean_latex_text(match.group(2))
            start = match.end()
            
            # Find content until next section or end
            if i < len(matches) - 1:
                end = matches[i + 1].start()
                section_content = content[start:end]
            else:
                section_content = content[start:]
            
            sections.append({
                'title': title,
                'level': level,
                'content': self.clean_latex_text(section_content),
                'raw_content': section_content
            })
        
        return sections
    
    def extract_figures(self, content: str) -> List[Dict[str, str]]:
        """Extract figure environments."""
        figures = []
        pattern = r'\\begin\{figure\*?\}(.*?)\\end\{figure\*?\}'
        
        for match in re.finditer(pattern, content, re.DOTALL | re.IGNORECASE):
            fig_content = match.group(1)
            
            # Extract caption
            caption_match = re.search(r'\\caption\{([^}]*)\}', fig_content, re.DOTALL)
            caption = self.clean_latex_text(caption_match.group(1)) if caption_match else ""
            
            # Extract label
            label_match = re.search(r'\\label\{([^}]*)\}', fig_content)
            label = label_match.group(1) if label_match else ""
            
            # Extract image filename
            include_match = re.search(r'\\includegraphics(?:\[.*?\])?\{([^}]*)\}', fig_content)
            image_file = include_match.group(1) if include_match else ""
            
            figures.append({
                'caption': caption,
                'label': label,
                'image_file': image_file,
                'raw': fig_content
            })
        
        return figures
    
    def extract_algorithms(self, content: str) -> List[Dict[str, str]]:
        """Extract algorithm environments."""
        algorithms = []
        
        # Match both algorithm and algorithmic environments
        pattern = r'\\begin\{algorithm\*?\}(.*?)\\end\{algorithm\*?\}'
        
        for match in re.finditer(pattern, content, re.DOTALL | re.IGNORECASE):
            alg_content = match.group(1)
            
            # Extract caption
            caption_match = re.search(r'\\caption\{([^}]*)\}', alg_content, re.DOTALL)
            caption = self.clean_latex_text(caption_match.group(1)) if caption_match else ""
            
            # Extract label
            label_match = re.search(r'\\label\{([^}]*)\}', alg_content)
            label = label_match.group(1) if label_match else ""
            
            algorithms.append({
                'caption': caption,
                'label': label,
                'content': self.clean_latex_text(alg_content),
                'raw': alg_content
            })
        
        return algorithms
    
    def extract_tables(self, content: str) -> List[Dict[str, str]]:
        """Extract table environments."""
        tables = []
        pattern = r'\\begin\{table\*?\}(.*?)\\end\{table\*?\}'
        
        for match in re.finditer(pattern, content, re.DOTALL | re.IGNORECASE):
            table_content = match.group(1)
            
            # Extract caption
            caption_match = re.search(r'\\caption\{([^}]*)\}', table_content, re.DOTALL)
            caption = self.clean_latex_text(caption_match.group(1)) if caption_match else ""
            
            # Extract label
            label_match = re.search(r'\\label\{([^}]*)\}', table_content)
            label = label_match.group(1) if label_match else ""
            
            # Extract tabular content
            tabular_match = re.search(r'\\begin\{tabular\}(.*?)\\end\{tabular\}', table_content, re.DOTALL)
            tabular = tabular_match.group(1) if tabular_match else ""
            
            tables.append({
                'caption': caption,
                'label': label,
                'tabular': self.clean_latex_text(tabular),
                'raw': table_content
            })
        
        return tables
    
    def extract_citations(self, content: str) -> List[str]:
        """Extract all citations."""
        citations = []
        
        # Pattern for \cite{key1,key2} and \citep, \citet variants
        pattern = r'\\(?:cite|citep|citet|citeauthor|citeyear)\{([^}]*)\}'
        
        for match in re.finditer(pattern, content):
            keys = match.group(1).split(',')
            citations.extend([k.strip() for k in keys])
        
        return list(set(citations))  # Remove duplicates
    
    def extract_references(self, content: str) -> List[Dict[str, str]]:
        """Extract bibliography entries."""
        references = []
        
        # Pattern for \bibitem{key} ...
        pattern = r'\\bibitem(?:\[(.*?)\])?\{(.*?)\}(.*?)(?=\\bibitem|$)'
        
        for match in re.finditer(pattern, content, re.DOTALL):
            label = match.group(1) if match.group(1) else ""
            key = match.group(2)
            bib_content = self.clean_latex_text(match.group(3))
            
            references.append({
                'key': key,
                'label': label,
                'content': bib_content
            })
        
        return references
    
    def extract_equations(self, content: str) -> List[Dict[str, str]]:
        """Extract equation environments."""
        equations = []
        
        # Match various equation environments
        patterns = [
            (r'\\begin\{equation\*?\}(.*?)\\end\{equation\*?\}', 'equation'),
            (r'\\begin\{align\*?\}(.*?)\\end\{align\*?\}', 'align'),
            (r'\\begin\{gather\*?\}(.*?)\\end\{gather\*?\}', 'gather'),
            (r'\\\[(.*?)\\\]', 'displaymath'),
        ]
        
        for pattern, env_type in patterns:
            for match in re.finditer(pattern, content, re.DOTALL):
                equations.append({
                    'type': env_type,
                    'content': match.group(1).strip(),
                    'raw': match.group(0)
                })
        
        return equations
    
    def extract_packages(self, content: str) -> List[str]:
        """Extract all used packages."""
        packages = []
        pattern = r'\\usepackage(?:\[.*?\])?\{([^}]*)\}'
        
        for match in re.finditer(pattern, content):
            pkg_list = match.group(1).split(',')
            packages.extend([p.strip() for p in pkg_list])
        
        return packages
    
    def clean_latex_text(self, text: str) -> str:
        """
        Clean LaTeX commands and formatting from text.
        """
        if not text:
            return ""
        
        # Remove comments
        text = re.sub(r'(?<!\\)%.*?\n', '\n', text)
        
        # Remove common commands but keep their content
        commands_to_remove = [
            r'\\emph\{([^}]*)\}',
            r'\\textbf\{([^}]*)\}',
            r'\\textit\{([^}]*)\}',
            r'\\texttt\{([^}]*)\}',
            r'\\textsc\{([^}]*)\}',
            r'\\mathrm\{([^}]*)\}',
            r'\\label\{[^}]*\}',
            r'\\ref\{[^}]*\}',
            r'\\cite[^{]*\{[^}]*\}',
            r'\\url\{([^}]*)\}',
            r'\\href\{[^}]*\}\{([^}]*)\}',
        ]
        
        for pattern in commands_to_remove:
            text = re.sub(pattern, r'\1', text)
        
        # Replace special characters
        replacements = {
            r'\\&': '&',
            r'\\%': '%',
            r'\\$': '$',
            r'\\#': '#',
            r'\\_': '_',
            r'\\{': '{',
            r'\\}': '}',
            r'\\textbackslash': '\\',
            r'\\~': '~',
            r'\\^': '^',
            r'\\ldots': '...',
            r'\\dots': '...',
            r'\\LaTeX': 'LaTeX',
            r'\\TeX': 'TeX',
            '~': ' ',
        }
        
        for latex, char in replacements.items():
            text = text.replace(latex, char)
        
        # Remove remaining commands
        text = re.sub(r'\\[a-zA-Z]+\*?(?:\[[^\]]*\])?(?:\{[^}]*\})?', ' ', text)
        
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text
    
    def parse(self, tex_file: Path) -> Dict:
        """
        Parse a complete LaTeX file and return structured information.
        """
        content = self.read_tex_file(tex_file)
        
        # Resolve all inputs
        resolved_content = self.resolve_inputs(content, tex_file.parent)
        
        # Remove preamble for content extraction
        doc_match = re.search(r'\\begin\{document\}(.*?)\\end\{document\}', 
                              resolved_content, re.DOTALL | re.IGNORECASE)
        
        if doc_match:
            doc_content = doc_match.group(1)
        else:
            doc_content = resolved_content
        
        return {
            'documentclass': self.extract_documentclass(resolved_content),
            'title': self.extract_title(resolved_content),
            'authors': self.extract_authors(resolved_content),
            'abstract': self.extract_abstract(resolved_content),
            'sections': self.extract_sections(doc_content),
            'figures': self.extract_figures(doc_content),
            'tables': self.extract_tables(doc_content),
            'algorithms': self.extract_algorithms(doc_content),
            'equations': self.extract_equations(doc_content),
            'citations': self.extract_citations(doc_content),
            'packages': self.extract_packages(resolved_content),
        }


def main():
    """CLI for testing the parser."""
    import argparse
    import json
    
    parser = argparse.ArgumentParser(description='Parse LaTeX file')
    parser.add_argument('tex_file', help='Path to .tex file')
    parser.add_argument('--output', '-o', help='Output JSON file')
    parser.add_argument('--verbose', '-v', action='store_true')
    
    args = parser.parse_args()
    
    parser = LatexParser(verbose=args.verbose)
    result = parser.parse(Path(args.tex_file))
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"Title: {result['title']}")
    print(f"Authors: {len(result['authors'])}")
    print(f"Sections: {len(result['sections'])}")
    print(f"Figures: {len(result['figures'])}")
    print(f"Tables: {len(result['tables'])}")
    print(f"Algorithms: {len(result['algorithms'])}")
    print(f"Citations: {len(result['citations'])}")
    print(f"{'='*60}")
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"Output saved to: {args.output}")


if __name__ == "__main__":
    main()
