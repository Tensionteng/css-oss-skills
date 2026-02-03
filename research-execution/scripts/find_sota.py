#!/usr/bin/env python3
"""
Find SOTA papers for a specific task/dataset.

Dependencies:
    uv add semanticscholar requests

Usage:
    # Search for SOTA on specific dataset
    uv run python scripts/find_sota.py --task "math reasoning" --dataset "GSM8K"
    
    # Search with year filter
    uv run python scripts/find_sota.py --task "chain of thought" --years 2023-2025
    
    # Output to file
    uv run python scripts/find_sota.py --task "reasoning" --output .research/sota-candidates.json
"""

import argparse
import json
import sys
from datetime import datetime

try:
    from semanticscholar import SemanticScholar
except ImportError:
    print("Error: semanticscholar not installed. Run: uv add semanticscholar")
    sys.exit(1)


def find_sota_papers(task: str, dataset: str = None, year_range: tuple = None, min_citations: int = 20, limit: int = 10):
    """
    Search for high-quality papers in a specific area.
    
    Strategy:
    1. Search for papers matching task + dataset
    2. Filter by year range (for recency)
    3. Sort by citation count (for impact/recognition)
    4. Return top candidates with metadata
    """
    sch = SemanticScholar()
    
    # Build query
    query_parts = [task]
    if dataset:
        query_parts.append(dataset)
    query = " ".join(query_parts)
    
    print(f"Searching for: {query}")
    if year_range:
        print(f"Year range: {year_range[0]}-{year_range[1]}")
    print(f"Min citations: {min_citations}")
    print("-" * 60)
    
    # Search
    results = sch.search_paper(query, limit=limit * 2)  # Get more to filter
    papers = list(results)
    
    # Filter and sort
    filtered = []
    for p in papers:
        # Year filter
        if year_range and p.year:
            if not (year_range[0] <= p.year <= year_range[1]):
                continue
        
        # Citation filter
        citations = p.citationCount or 0
        if citations < min_citations:
            continue
        
        filtered.append({
            "title": p.title,
            "authors": [a.name for a in (p.authors or [])[:3]],
            "year": p.year,
            "paperId": p.paperId,
            "citationCount": citations,
            "abstract": (p.abstract or "")[:300] + "..." if p.abstract and len(p.abstract) > 300 else (p.abstract or ""),
            "fields": p.fieldsOfStudy or [],
            "venue": p.venue or "Unknown",
        })
    
    # Sort by citations
    filtered.sort(key=lambda x: x["citationCount"], reverse=True)
    
    return filtered[:limit]


def assess_as_baseline(papers, task):
    """Provide assessment of papers as baseline candidates."""
    if not papers:
        return "No papers found matching criteria."
    
    lines = [
        "\n" + "=" * 60,
        "BASELINE ASSESSMENT",
        "=" * 60,
        f"Found {len(papers)} candidate papers\n",
    ]
    
    for i, p in enumerate(papers, 1):
        lines.extend([
            f"\n[{i}] {p['title']}",
            f"    Authors: {', '.join(p['authors'][:3])}",
            f"    Year: {p['year']}, Citations: {p['citationCount']}",
            f"    Venue: {p['venue']}",
            f"    Abstract: {p['abstract'][:150]}...",
        ])
    
    # Recommendations
    lines.extend([
        "\n" + "-" * 60,
        "RECOMMENDATIONS",
        "-" * 60,
    ])
    
    if papers:
        top = papers[0]
        lines.append(f"\n🏆 Top candidate: {top['title'][:50]}...")
        lines.append(f"   High citations ({top['citationCount']}) suggest established method")
        lines.append(f"   Verify: Is this the current SOTA for your specific setting?")
    
    if len(papers) >= 2:
        recent = [p for p in papers if p['year'] and p['year'] >= 2024]
        if recent:
            lines.append(f"\n📅 Recent option: {recent[0]['title'][:50]}...")
            lines.append(f"   Year: {recent[0]['year']}, may represent newer approach")
    
    lines.append("\n💡 Next step: Use pdf-reader skill to analyze selected paper(s)")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Find SOTA baseline papers")
    parser.add_argument("--task", required=True, help="Research task (e.g., 'math reasoning')")
    parser.add_argument("--dataset", help="Specific dataset (e.g., 'GSM8K')")
    parser.add_argument("--years", help="Year range (e.g., '2023-2025')")
    parser.add_argument("--min-citations", type=int, default=20, help="Minimum citations")
    parser.add_argument("--limit", type=int, default=10, help="Max results")
    parser.add_argument("--output", help="Output JSON file")
    
    args = parser.parse_args()
    
    # Parse year range
    year_range = None
    if args.years:
        start, end = args.years.split("-")
        year_range = (int(start), int(end))
    else:
        # Default: last 3 years
        current_year = datetime.now().year
        year_range = (current_year - 2, current_year + 1)
    
    # Search
    papers = find_sota_papers(
        task=args.task,
        dataset=args.dataset,
        year_range=year_range,
        min_citations=args.min_citations,
        limit=args.limit
    )
    
    # Print assessment
    print(assess_as_baseline(papers, args.task))
    
    # Save to file if requested
    if args.output and papers:
        with open(args.output, 'w') as f:
            json.dump({
                "query": {"task": args.task, "dataset": args.dataset, "years": year_range},
                "candidates": papers,
                "timestamp": datetime.now().isoformat(),
            }, f, indent=2)
        print(f"\n✓ Saved to {args.output}")


if __name__ == "__main__":
    main()
