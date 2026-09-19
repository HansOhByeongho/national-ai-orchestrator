from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
def test_health():
 r=client.get("/health"); assert r.status_code==200; assert r.json()["version"]=="4.0.0"
def test_home():
 r=client.get("/"); assert r.status_code==200; assert "v4.0" in r.text
def test_domain_routing():
 r=client.post("/orchestrate",json={"user":"analyst","question":"철도 역세권 법령 국비 교통 수요 GIS 환경 데이터 분석"})
 assert r.status_code==200
 j=r.json(); assert len(j["plan"])>=5; assert "mcp_results" in j; assert "quality" in j["verification"]
def test_knowledge_endpoint():
 r=client.get("/knowledge"); assert r.status_code==200
def test_rbac():
 r=client.post("/tool/call",json={"role":"analyst","tool":"write_external","payload":{}})
 assert r.json()["status"]=="denied"
