def test_ping_endpoints(client):
    for path in (
        "/api/ingest/ping",
        "/api/classify/ping",
        "/api/releases/ping",
        "/ping",
    ):
        resp = client.get(path)
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["ok"] is True
