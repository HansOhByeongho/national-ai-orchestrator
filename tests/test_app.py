from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)
def test_health(): assert client.get("/health").json()["status"] == "ok"
def test_orchestrate():
    r = client.post("/orchestrate", json={"user":"analyst","question":"정책 법령 데이터 분석"})
    assert r.status_code == 200
    assert len(r.json()["plan"]) >= 1
def test_rbac():
    r = client.post("/tool/call", json={"role":"analyst","tool":"write_external","payload":{}})
    assert r.json()["status"] == "denied"
