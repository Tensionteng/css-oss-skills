#!/usr/bin/env python3
"""
Update review history tracking.

This script helps manage the REVIEW-HISTORY.md file by:
1. Reading previous review rounds
2. Comparing with current REVIEW.md
3. Tracking which issues are fixed/persistent
4. Updating history file

Dependencies:
    uv add pyyaml

Usage:
    # After generating new REVIEW.md, update history:
    uv run python scripts/update_history.py --round 2
    
    # Or with explicit paths:
    uv run python scripts/update_history.py \
        --round 2 \
        --current .research/REVIEW.md \
        --history .research/REVIEW-HISTORY.md
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: pyyaml not installed. Run: uv add pyyaml")
    sys.exit(1)


def parse_review_file(review_path: str) -> dict:
    """Parse REVIEW.md to extract issues and metadata."""
    content = Path(review_path).read_text()
    
    # Extract round number
    round_match = re.search(r'Round\s+(\d+)', content)
    round_num = int(round_match.group(1)) if round_match else 1
    
    # Extract date
    date_match = re.search(r'Date:\s*(\d{4}-\d{2}-\d{2})', content)
    date = date_match.group(1) if date_match else datetime.now().strftime("%Y-%m-%d")
    
    # Extract overall rating
    rating_match = re.search(r'Verdict:\s*(.+)', content)
    rating = rating_match.group(1).strip() if rating_match else "Unknown"
    
    # Extract issues by severity
    issues = {
        "critical": [],
        "major": [],
        "minor": [],
        "trivial": []
    }
    
    # Pattern: ### [ID]: [Title] with severity in context
    current_severity = None
    for line in content.split('\n'):
        # Check for severity headers
        if 'Critical Issues' in line:
            current_severity = "critical"
        elif 'Major Issues' in line:
            current_severity = "major"
        elif 'Minor Issues' in line:
            current_severity = "minor"
        elif 'Trivial' in line:
            current_severity = "trivial"
        
        # Extract issue ID and title
        match = re.match(r'###\s+(C|M|m|t)?(\d+):\s*(.+)', line)
        if match and current_severity:
            severity_prefix = match.group(1) or ''
            num = match.group(2)
            title = match.group(3).strip()
            issue_id = f"R{round_num}.{severity_prefix}{num}"
            issues[current_severity].append({
                "id": issue_id,
                "title": title,
                "round": round_num,
                "severity": current_severity
            })
    
    return {
        "round": round_num,
        "date": date,
        "rating": rating,
        "issues": issues
    }


def load_history(history_path: str) -> dict:
    """Load existing history or create new."""
    path = Path(history_path)
    if not path.exists():
        return {
            "current_status": {},
            "rounds": []
        }
    
    # Parse markdown (simplified)
    content = path.read_text()
    # TODO: Implement full parser
    return {"raw": content}


def generate_history_entry(current_review: dict, previous_rounds: list) -> str:
    """Generate markdown entry for this round."""
    round_num = current_review["round"]
    date = current_review["date"]
    rating = current_review["rating"]
    
    lines = [
        f"## Round {round_num} ({date})",
        f"**Status**: {rating}",
        "",
        "### Issues Found",
        "| ID | Issue | Severity | Status |",
        "|----|-------|----------|--------|",
    ]
    
    # Add all issues
    for severity in ["critical", "major", "minor", "trivial"]:
        for issue in current_review["issues"][severity]:
            lines.append(f"| {issue['id']} | {issue['title']} | {severity.capitalize()} | 🔧 To Fix |")
    
    total_issues = sum(len(v) for v in current_review["issues"].values())
    lines.extend([
        "",
        f"**Total Issues**: {total_issues}",
        f"- Critical: {len(current_review['issues']['critical'])}",
        f"- Major: {len(current_review['issues']['major'])}",
        f"- Minor: {len(current_review['issues']['minor'])}",
        f"- Trivial: {len(current_review['issues']['trivial'])}",
        "",
    ])
    
    # If Round 2+, verify previous issues
    if round_num > 1 and previous_rounds:
        lines.extend([
            "### Verification of Previous Issues",
            "[To be filled in after manual verification]",
            "",
            "Example:",
            "- R1.1: ✓ Fixed - description of fix",
            "- R1.2: ⚠️ Partial - still some issues",
            "- R1.3: ✗ Not fixed - still present",
            "",
        ])
    
    # Persistent issues section
    lines.extend([
        "### Persistent Issues",
        "[Issues that appear in multiple rounds - indicates deeper problems]",
        "",
    ])
    
    # Trend analysis
    lines.extend([
        "### Trend Analysis",
        f"- This round: {total_issues} issues found",
        "- Comparison to previous: [To fill in]",
        "- Trajectory: [Improving / Stagnant / Worsening]",
        "",
    ])
    
    return '\n'.join(lines)


def update_history_file(history_path: str, new_entry: str, current_round: int):
    """Update or create history file."""
    path = Path(history_path)
    
    if path.exists():
        content = path.read_text()
        # Update current status section
        status_section = f"""## Current Status
**Latest Round**: {current_round}
**Date**: {datetime.now().strftime("%Y-%m-%d")}
**Overall**: [TBD]
**Trend**: [TBD]

---

"""
        # Insert after header
        if "## Current Status" in content:
            # Replace existing status
            content = re.sub(
                r'## Current Status.*?---',
                status_section.rstrip(),
                content,
                flags=re.DOTALL
            )
        else:
            # Add after title
            content = content.replace(
                "# Review History",
                "# Review History\n\n" + status_section
            )
        
        # Add new round entry
        content = content + '\n' + new_entry
    else:
        # Create new file
        content = f"""# Review History

## Current Status
**Latest Round**: {current_round}
**Date**: {datetime.now().strftime("%Y-%m-%d")}
**Overall**: [TBD - update after review]
**Trend**: [TBD - Improving / Stagnant / Worsening]

---

{new_entry}

---

## Trends & Insights

### Recurring Themes
[Issues that appear across multiple rounds]

### Quality Trajectory
[Review sentiment across rounds]

### Readiness Checklist
- [ ] All critical issues resolved
- [ ] All major issues resolved  
- [ ] Only minor/trivial issues remain
- [ ] Ready for real submission
"""
    
    path.write_text(content)
    print(f"Updated {history_path}")


def main():
    parser = argparse.ArgumentParser(description="Update review history")
    parser.add_argument("--round", type=int, required=True, help="Review round number")
    parser.add_argument("--current", default=".research/REVIEW.md", help="Current review file")
    parser.add_argument("--history", default=".research/REVIEW-HISTORY.md", help="History file")
    parser.add_argument("--dry-run", action="store_true", help="Print only, don't write")
    
    args = parser.parse_args()
    
    # Parse current review
    if not Path(args.current).exists():
        print(f"Error: Current review not found: {args.current}")
        sys.exit(1)
    
    current = parse_review_file(args.current)
    
    # Load previous history (if exists)
    previous = []
    if Path(args.history).exists():
        previous = load_history(args.history)
    
    # Generate new entry
    new_entry = generate_history_entry(current, previous)
    
    if args.dry_run:
        print("=== NEW HISTORY ENTRY ===")
        print(new_entry)
        print("=========================")
    else:
        update_history_file(args.history, new_entry, args.round)
        
        # Print summary
        total = sum(len(v) for v in current["issues"].values())
        print(f"\nRound {args.round} Summary:")
        print(f"  Total issues: {total}")
        print(f"  Critical: {len(current['issues']['critical'])}")
        print(f"  Major: {len(current['issues']['major'])}")
        print(f"  Minor: {len(current['issues']['minor'])}")
        print(f"\nNext steps:")
        print("  1. Fix issues identified in REVIEW.md")
        print("  2. After fixing, update REVIEW-HISTORY.md with verification status")
        print("  3. Prepare next draft for Round", args.round + 1)


if __name__ == "__main__":
    main()
