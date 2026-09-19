from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)

def test_health():
    r=client.get("/health")
    assert r.status_code==200
    assert r.json()["version"]=="2.0.0"

def test_home():
    r=client.get("/")
    assert r.status_code==200
    assert "National AI Orchestrator v2.0" in r.text

def test_orchestrate():
    r=client.post("/orchestrate",json={"user":"analyst","question":"정책 법령 데이터 분석"})
    assert r.status_code==200
    j=r.json()
    assert len(j["plan"])>=1
    assert "final_answer" in j

def test_rbac():
    r=client.post("/tool/call",json={"role":"analyst","tool":"write_external","payload":{}})
    assert r.json()["status"]=="denied"
