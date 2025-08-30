from app.services.importer_git import parse_git_log


def test_parse_git_log_basic():
    sample = "\n".join(
        [
            "abc123|Alice|2025-08-01T10:20:30+00:00|feat(api): add search",
            "def456|Bob|2025-08-02T11:22:33+00:00|fix: handle empty input",
        ]
    )
    items = parse_git_log(sample)
    assert len(items) == 2
    assert items[0]["sha"] == "abc123"
    assert items[0]["author"] == "Alice"
    assert items[0]["title"].startswith("feat")
    assert items[0]["merged_at"].isoformat() == "2025-08-01T10:20:30+00:00"
