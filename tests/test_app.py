from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
def test_health():
 r=client.get("/health"); assert r.status_code==200; assert r.json()["version"]=="8.0.0"
def test_home():
 r=client.get("/"); assert r.status_code==200; assert "v8.0" in r.text
def test_domain_routing():
 r=client.post("/orchestrate",json={"user":"analyst","question":"철도 역세권 법령 국비 교통 수요 GIS 환경 데이터 분석"})
 assert r.status_code==200
 j=r.json(); assert len(j["plan"])>=5; assert "mcp_results" in j; assert "quality" in j["verification"]
def test_knowledge_endpoint():
 r=client.get("/knowledge"); assert r.status_code==200
def test_rbac():
 r=client.post("/tool/call",json={"role":"analyst","tool":"write_external","payload":{}})
 assert r.json()["status"]=="denied"

def test_spatial_math():
 from app.analytics.spatial import haversine_km
 assert haversine_km(37.68424,127.85391,37.62145,127.76612)>0
def test_finance_math():
 from app.analytics.finance import funding_mix
 assert funding_mix(100,{"national":70,"local":30})["amounts"]["national"]==70

def test_public_catalog():
 from app.knowledge.catalog import load_catalog
 assert len(load_catalog()) >= 8
def test_hongcheon_case_file():
 import json
 from pathlib import Path
 p=Path("case_studies/hongcheon.json")
 d=json.loads(p.read_text(encoding="utf-8"))
 assert len(d["stations"])==2
