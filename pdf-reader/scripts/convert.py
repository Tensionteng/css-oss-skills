#!/usr/bin/env python3
"""
Convert PDF pages to images for AI analysis.

Dependencies:
    uv add pymupdf

Usage:
    # Convert entire PDF
    uv run python pdf_to_images.py --arxiv 2405.12345 --output ./paper-images/
    
    # Convert specific pages (e.g., figures/tables)
    uv run python pdf_to_images.py --arxiv 2405.12345 --pages 1,3,5-8 --output ./key-pages/
    
    # From local PDF
    uv run python pdf_to_images.py --pdf /path/to/paper.pdf --output ./images/
"""

import argparse
import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Error: pymupdf not installed. Run: uv add pymupdf")
    sys.exit(1)


def download_arxiv_pdf(arxiv_id: str) -> str:
    """Download arXiv PDF to temp location."""
    import requests
    
    url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    print(f"Downloading from {url}...")
    
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    
    temp_path = f"/tmp/{arxiv_id.replace('/', '_')}.pdf"
    with open(temp_path, "wb") as f:
        f.write(response.content)
    
    print(f"Downloaded to {temp_path}")
    return temp_path


def parse_page_range(pages_str: str) -> list:
    """Parse page range like '1,3,5-10' to list of indices (0-based)."""
    pages = []
    for part in pages_str.split(','):
        if '-' in part:
            start, end = part.split('-')
            pages.extend(range(int(start)-1, int(end)))  # Convert to 0-based
        else:
            pages.append(int(part)-1)  # Convert to 0-based
    return sorted(set(pages))


def pdf_to_images(pdf_path: str, output_dir: str, pages: list = None, zoom: int = 2):
    """
    Convert PDF pages to images.
    
    Args:
        pdf_path: Path to PDF file
        output_dir: Output directory for images
        pages: List of page indices (0-based), None for all
        zoom: Zoom factor for better quality (1=72dpi, 2=144dpi, etc.)
    """
    doc = fitz.open(pdf_path)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Determine pages to process
    if pages is None:
        pages = range(len(doc))
    else:
        # Filter valid pages
        pages = [p for p in pages if 0 <= p < len(doc)]
    
    print(f"Converting {len(pages)} pages to images...")
    
    # Set up matrix for higher resolution
    mat = fitz.Matrix(zoom, zoom)
    
    image_paths = []
    for page_num in pages:
        page = doc[page_num]
        
        # Render page to image
        pix = page.get_pixmap(matrix=mat)
        
        # Save image
        image_path = output_path / f"page_{page_num + 1:03d}.png"
        pix.save(str(image_path))
        image_paths.append(image_path)
        
        print(f"  Saved: {image_path.name}")
    
    doc.close()
    
    print(f"\nDone! {len(image_paths)} images saved to {output_dir}")
    return image_paths


def extract_figures_only(pdf_path: str, output_dir: str):
    """
    Extract only embedded images from PDF (not full page screenshots).
    Useful for getting high-res figures separately.
    """
    doc = fitz.open(pdf_path)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    figure_count = 0
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        images = page.get_images(full=True)
        
        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            
            figure_count += 1
            img_path = output_path / f"figure_{figure_count:03d}_page{page_num + 1}.{image_ext}"
            
            with open(img_path, "wb") as f:
                f.write(image_bytes)
            
            print(f"  Saved figure: {img_path.name}")
    
    doc.close()
    print(f"\nExtracted {figure_count} embedded figures to {output_dir}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert PDF to images for AI analysis"
    )
    
    # Input source
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--arxiv", help="arXiv ID (e.g., 2405.12345)")
    input_group.add_argument("--pdf", help="Path to local PDF file")
    
    # Output
    parser.add_argument("--output", "-o", required=True, 
                       help="Output directory for images")
    
    # Page selection
    parser.add_argument("--pages", 
                       help="Pages to convert (e.g., '1,3,5-10'). Default: all pages")
    
    # Quality
    parser.add_argument("--zoom", type=int, default=2,
                       help="Zoom factor (1=72dpi, 2=144dpi, 3=216dpi). Default: 2")
    
    # Mode
    parser.add_argument("--figures-only", action="store_true",
                       help="Extract only embedded figures, not full pages")
    
    args = parser.parse_args()
    
    # Get PDF
    if args.arxiv:
        pdf_path = download_arxiv_pdf(args.arxiv)
    else:
        pdf_path = args.pdf
        if not Path(pdf_path).exists():
            print(f"Error: PDF not found: {pdf_path}")
            sys.exit(1)
    
    # Parse page range
    pages = None
    if args.pages:
        pages = parse_page_range(args.pages)
        print(f"Will process pages: {[p+1 for p in pages]}")  # Convert back to 1-based for display
    
    # Convert
    if args.figures_only:
        extract_figures_only(pdf_path, args.output)
    else:
        pdf_to_images(pdf_path, args.output, pages, args.zoom)


if __name__ == "__main__":
    main()
