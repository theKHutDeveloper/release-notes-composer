def test_ingest_git_log(client):
    payload = "\n".join(
        [
            "aaa111|Alice|2025-08-01T10:20:30+00:00|feat(ui): add filters",
            "bbb222|Bob|2025-08-02T11:22:33+00:00|fix: null pointer",
        ]
    )
    resp = client.post("/api/ingest", json={"source": "git_log", "payload": payload})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["created"] == 2
    assert len(data["ids"]) == 2

    # idempotency: re-post same payload should not create duplicates
    resp2 = client.post("/api/ingest", json={"source": "git_log", "payload": payload})
    assert resp2.status_code == 200
    assert resp2.get_json()["created"] == 0
