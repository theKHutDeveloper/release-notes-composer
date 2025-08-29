def test_root_health(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}
