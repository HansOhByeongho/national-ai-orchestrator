import json
from pathlib import Path
CATALOG=Path(__file__).resolve().parents[2]/"knowledge_catalog"/"data_go_kr.json"
def datasets():
    return json.loads(CATALOG.read_text(encoding="utf-8"))["datasets"]
def by_agent(agent):
    return [d for d in datasets() if agent in d.get("agents",[])]
def configured():
    return [d for d in datasets() if d.get("enabled") and d.get("endpoint")]
