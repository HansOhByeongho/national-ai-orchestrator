import json, math, os, re
from pathlib import Path
from urllib.request import Request, urlopen
from pypdf import PdfReader
from docx import Document

ROOT=Path("data")
ROOT.mkdir(exist_ok=True)
DB=ROOT/"knowledge.json"

def _load():
    if DB.exists():
        try:return json.loads(DB.read_text(encoding="utf-8"))
        except Exception:return []
    return []

def _save(rows): DB.write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding="utf-8")

def _chunk(text,size=900,overlap=150):
    text=re.sub(r"\s+"," ",text).strip()
    if not text:return []
    out=[]; start=0
    while start<len(text):
        out.append(text[start:start+size])
        if start+size>=len(text):break
        start+=size-overlap
    return out

def extract(path:Path):
    ext=path.suffix.lower()
    if ext==".pdf": return "\n".join((p.extract_text() or "") for p in PdfReader(str(path)).pages)
    if ext==".docx": return "\n".join(p.text for p in Document(str(path)).paragraphs)
    if ext in (".txt",".md"): return path.read_text(encoding="utf-8",errors="ignore")
    raise ValueError("지원 형식: PDF, DOCX, TXT, MD")

def _embed(texts):
    key=os.getenv("OPENAI_API_KEY")
    if not key:return None
    body=json.dumps({"model":os.getenv("OPENAI_EMBEDDING_MODEL","text-embedding-3-small"),"input":texts}).encode()
    req=Request("https://api.openai.com/v1/embeddings",data=body,headers={"Authorization":f"Bearer {key}","Content-Type":"application/json"})
    with urlopen(req,timeout=90) as r:data=json.loads(r.read())
    return [x["embedding"] for x in data["data"]]

def ingest(path:Path,source:str):
    chunks=_chunk(extract(path)); vecs=_embed(chunks)
    rows=_load()
    rows=[r for r in rows if r.get("source")!=source]
    for i,c in enumerate(chunks):rows.append({"source":source,"chunk":i,"text":c,"embedding":vecs[i] if vecs else None})
    _save(rows)
    return {"source":source,"chunks":len(chunks),"semantic_embeddings":bool(vecs)}

def _cos(a,b):
    s=sum(x*y for x,y in zip(a,b)); na=math.sqrt(sum(x*x for x in a)); nb=math.sqrt(sum(x*x for x in b))
    return s/(na*nb) if na and nb else 0

def search(query,k=6):
    rows=_load()
    if not rows:return []
    qv=_embed([query])
    if qv and any(r.get("embedding") for r in rows):
        ranked=sorted(rows,key=lambda r:_cos(qv[0],r.get("embedding") or [0]*len(qv[0])),reverse=True)
    else:
        terms=set(re.findall(r"[가-힣A-Za-z0-9]+",query.lower()))
        ranked=sorted(rows,key=lambda r:sum(t in r["text"].lower() for t in terms),reverse=True)
    return [{"source":r["source"],"chunk":r["chunk"],"text":r["text"]} for r in ranked[:k]]

def stats():
    rows=_load(); return {"chunks":len(rows),"sources":sorted(set(r["source"] for r in rows))}
