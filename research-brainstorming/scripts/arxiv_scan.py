#!/usr/bin/env python3
"""
Quick arXiv literature scan for research brainstorming.

Dependencies:
    uv add arxiv

Usage:
    uv run python arxiv_scan.py "chain of thought reasoning" --max-results 10 --days 365
"""

import argparse
import sys
from datetime import datetime, timedelta

try:
    import arxiv
except ImportError:
    print("Error: arxiv package not installed. Run: uv add arxiv")
    sys.exit(1)


def search_arxiv(query: str, max_results: int = 10, days: int = None):
    """Search arXiv and return relevant papers."""
    
    # Build search query
    if days:
        # Filter by date
        client = arxiv.Client()
        search = arxiv.Search(
            query=query,
            max_results=max_results * 3,  # Get more to filter by date
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending,
        )
        papers = list(client.results(search))
        
        cutoff_date = datetime.now() - timedelta(days=days)
        papers = [p for p in papers if p.published.replace(tzinfo=None) > cutoff_date]
        papers = papers[:max_results]
    else:
        client = arxiv.Client()
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance,
        )
        papers = list(client.results(search))
    
    return papers


def format_paper(paper, index: int) -> str:
    """Format a paper for display."""
    lines = [
        f"\n{'='*60}",
        f"[{index}] {paper.title}",
        f"{'='*60}",
        f"Authors: {', '.join(str(a) for a in paper.authors[:3])}",
        f"Published: {paper.published.strftime('%Y-%m-%d')}",
        f"arXiv ID: {paper.get_short_id()}",
        f"URL: {paper.pdf_url}",
        f"\nAbstract (truncated):",
        f"{paper.summary[:300]}..." if len(paper.summary) > 300 else paper.summary,
        f"\nPrimary Category: {paper.primary_category}",
    ]
    return '\n'.join(lines)


def assess_relevance(papers, query: str) -> str:
    """Provide a quick relevance assessment."""
    if not papers:
        return "No papers found for this query."
    
    # Simple heuristic assessment
    categories = {}
    years = {}
    for p in papers:
        cat = p.primary_category.split('.')[0]
        categories[cat] = categories.get(cat, 0) + 1
        year = p.published.year
        years[year] = years.get(year, 0) + 1
    
    assessment = [
        "\n" + "="*60,
        "RELEVANCE ASSESSMENT",
        "="*60,
        f"Total papers found: {len(papers)}",
        f"\nBy Category: {categories}",
        f"By Year: {years}",
    ]
    
    # Activity level
    recent_count = sum(1 for p in papers if p.published.year >= 2024)
    if recent_count >= len(papers) * 0.7:
        activity = "Very Active (70%+ from 2024+)"
    elif recent_count >= len(papers) * 0.4:
        activity = "Active (40-70% from 2024+)"
    else:
        activity = "Moderate (<40% from 2024+)"
    
    assessment.append(f"\nActivity Level: {activity}")
    
    # Novelty assessment
    if len(papers) > 20:
        assessment.append("⚠️  Crowded space - need strong differentiation")
    elif len(papers) < 3:
        assessment.append("⚠️  Sparse space - verify this is a real problem")
    else:
        assessment.append("✓ Balanced space - look for specific gaps")
    
    return '\n'.join(assessment)


def main():
    parser = argparse.ArgumentParser(description="Quick arXiv scan for research brainstorming")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--max-results", type=int, default=10, help="Max papers to return")
    parser.add_argument("--days", type=int, help="Only papers from last N days")
    
    args = parser.parse_args()
    
    print(f"Searching arXiv for: '{args.query}'")
    print(f"Max results: {args.max_results}")
    if args.days:
        print(f"Time window: last {args.days} days")
    print("\n" + "="*60)
    
    try:
        papers = search_arxiv(args.query, args.max_results, args.days)
        
        if not papers:
            print("\nNo papers found. Try broadening your search terms.")
            return
        
        for i, paper in enumerate(papers, 1):
            print(format_paper(paper, i))
        
        print(assess_relevance(papers, args.query))
        
        # Suggest next queries
        print("\n" + "="*60)
        print("SUGGESTED FOLLOW-UP QUERIES")
        print("="*60)
        words = args.query.split()
        if len(words) > 2:
            print(f"1. '{' '.join(words[:2])} survey'")
            print(f"2. '{' '.join(words[:2])} review'")
        print(f"3. Add 'limitation' or 'challenge' to find gaps")
        print(f"4. Add specific method names (e.g., 'transformer', 'gpt')")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
