#!/usr/bin/env python3
"""
Semantic Scholar search for broader literature coverage.

Dependencies:
    uv add semanticscholar

Usage:
    uv run python s2_scan.py "large language model reasoning" --max-results 10
"""

import argparse
import sys

try:
    from semanticscholar import SemanticScholar
except ImportError:
    print("Error: semanticscholar package not installed. Run: uv add semanticscholar")
    sys.exit(1)


def search_s2(query: str, max_results: int = 10):
    """Search Semantic Scholar."""
    sch = SemanticScholar()
    results = sch.search_paper(query, limit=max_results)
    return list(results)


def format_paper(paper, index: int) -> str:
    """Format a paper for display."""
    authors = ', '.join([a.name for a in paper.authors[:3]]) if paper.authors else "Unknown"
    year = paper.year if paper.year else "Unknown"
    
    lines = [
        f"\n{'='*60}",
        f"[{index}] {paper.title}",
        f"{'='*60}",
        f"Authors: {authors}",
        f"Year: {year}",
        f"Paper ID: {paper.paperId}",
        f"Citation Count: {paper.citationCount or 0}",
    ]
    
    if paper.abstract:
        abstract = paper.abstract[:300] + "..." if len(paper.abstract) > 300 else paper.abstract
        lines.extend([f"\nAbstract:", abstract])
    
    if paper.fieldsOfStudy:
        lines.append(f"\nFields: {', '.join(paper.fieldsOfStudy)}")
    
    return '\n'.join(lines)


def assess_landscape(papers):
    """Assess the research landscape."""
    if not papers:
        return "No papers found."
    
    years = {}
    fields = {}
    citations = []
    
    for p in papers:
        if p.year:
            years[p.year] = years.get(p.year, 0) + 1
        if p.fieldsOfStudy:
            for f in p.fieldsOfStudy:
                fields[f] = fields.get(f, 0) + 1
        if p.citationCount:
            citations.append(p.citationCount)
    
    avg_citations = sum(citations) / len(citations) if citations else 0
    
    assessment = [
        "\n" + "="*60,
        "LANDSCAPE ASSESSMENT",
        "="*60,
        f"Total papers: {len(papers)}",
        f"Average citations: {avg_citations:.1f}",
        f"\nPublication years: {dict(sorted(years.items()))}",
        f"\nTop fields: {dict(sorted(fields.items(), key=lambda x: -x[1])[:5])}",
    ]
    
    # Identify highly cited papers
    if papers and any(p.citationCount for p in papers):
        top_cited = sorted([p for p in papers if p.citationCount], 
                          key=lambda x: x.citationCount or 0, reverse=True)[:3]
        assessment.append("\nKey Papers (by citation):")
        for p in top_cited:
            assessment.append(f"  - {p.title[:60]}... ({p.citationCount} citations)")
    
    return '\n'.join(assessment)


def main():
    parser = argparse.ArgumentParser(description="Semantic Scholar scan for research")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--max-results", type=int, default=10, help="Max papers to return")
    
    args = parser.parse_args()
    
    print(f"Searching Semantic Scholar for: '{args.query}'")
    print("="*60)
    
    try:
        papers = search_s2(args.query, args.max_results)
        
        if not papers:
            print("\nNo papers found. Try different keywords.")
            return
        
        for i, paper in enumerate(papers, 1):
            print(format_paper(paper, i))
        
        print(assess_landscape(papers))
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
