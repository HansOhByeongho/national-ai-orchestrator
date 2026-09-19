"""Optional Jev gate/router/reranker adapter.

JEV_BASE_URL should point to an OpenAI-compatible endpoint.
No credential or provider-specific URL is committed to GitHub.
If Jev is unavailable, the orchestrator safely falls back to deterministic routing.
"""
import json,os
import httpx

BASE=os.getenv("JEV_BASE_URL","").rstrip("/")
KEY=os.getenv("JEV_API_KEY","")
MODEL=os.getenv("JEV_MODEL","")
def configured(): return bool(BASE and MODEL)

async def _json(prompt):
 if not configured(): return None
 headers={"Content-Type":"application/json"}
 if KEY: headers["Authorization"]=f"Bearer {KEY}"
 payload={"model":MODEL,"messages":[{"role":"user","content":prompt}],"temperature":0,"response_format":{"type":"json_object"}}
 try:
  async with httpx.AsyncClient(timeout=30) as c:
   r=await c.post(f"{BASE}/chat/completions",headers=headers,json=payload); r.raise_for_status()
   return json.loads(r.json()["choices"][0]["message"]["content"])
 except Exception:
  return None

async def gate(question,allowed):
 prompt=f"""You are a routing gate. Return JSON only: {{"agents":[],"needs_retrieval":true,"risk":"low"}}.
Choose only from {allowed}. Question: {question}"""
 return await _json(prompt)

async def rerank(question,items,top_k=8):
 if not items:return []
 compact=[{"i":i,"source":x.get("source"),"text":x.get("text","")[:1200]} for i,x in enumerate(items)]
 prompt=f"""Rerank evidence for relevance to the question. Return JSON only: {{"order":[integer indexes]}}.
Question: {question}
Candidates: {json.dumps(compact,ensure_ascii=False)}"""
 out=await _json(prompt)
 if not out:return items[:top_k]
 order=[i for i in out.get("order",[]) if isinstance(i,int) and 0<=i<len(items)]
 seen=set(order); order+= [i for i in range(len(items)) if i not in seen]
 return [items[i] for i in order[:top_k]]
