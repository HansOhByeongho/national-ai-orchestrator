import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]/"knowledge_catalog"
def load_catalog(domain=None):
    paths=[ROOT/f"{domain}.json"] if domain else sorted(ROOT.glob("*.json"))
    out=[]
    for p in paths:
        if p.exists(): out.extend(json.loads(p.read_text(encoding="utf-8")))
    return out
def search_catalog(query,domain=None):
    q=query.lower()
    return [x for x in load_catalog(domain) if q in json.dumps(x,ensure_ascii=False).lower()]
