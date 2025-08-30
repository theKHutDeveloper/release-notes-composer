from __future__ import annotations

from datetime import datetime


def parse_git_log(text: str) -> list[dict]:
    """
    parse lines produced by:
      git log --date=iso-strict --pretty=format:%H|%an|%ad|%s

    returns a list of dicts:
      { "sha": str, "author": str, "merged_at": datetime, "title": str, "body": None }
    """
    items: list[dict] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split("|", 3)
        if len(parts) < 4:
            # skip malformed lines
            continue
        sha, author, date_str, title = parts
        # iso-strict looks like: 2025-08-30T12:34:56+01:00  (or ...Z)
        if date_str.endswith("Z"):
            date_str = date_str.replace("Z", "+00:00")
        merged_at = datetime.fromisoformat(date_str)
        items.append(
            {
                "sha": sha,
                "author": author,
                "merged_at": merged_at,
                "title": title,
                "body": None,
            }
        )
    return items
