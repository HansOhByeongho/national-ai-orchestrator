from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse\nfrom pathlib import Path\nimport tempfile, shutil\nfrom app.rag.store import ingest, stats
from pydantic import BaseModel, Field
from app.orchestrator import NationalAIOrchestrator
from app.mcp.gateway import MCPGateway
from app.security.controls import allow, requires_human_approval

app=FastAPI(title="National AI Orchestrator v3.0",version="3.0.0")
orchestrator=NationalAIOrchestrator(); gateway=MCPGateway()

class Request(BaseModel):
    user:str="analyst"
    question:str=Field(min_length=3)
class ToolRequest(BaseModel):
    role:str="analyst"; tool:str; payload:dict={}

@app.get("/",response_class=HTMLResponse)
def home():
    return """<!doctype html><html lang='ko'><meta charset='utf-8'><meta name='viewport' content='width=device-width'><title>National AI Orchestrator v3.0</title>
<style>body{font-family:system-ui;background:#f5f7fb;margin:0;color:#172033}.w{max-width:920px;margin:40px auto;padding:20px}.c{background:white;border-radius:20px;padding:26px;box-shadow:0 10px 35px #0001;margin-bottom:18px}textarea{width:100%;min-height:130px;padding:14px;box-sizing:border-box;border:1px solid #ccd3df;border-radius:12px;font-size:16px}button{background:#172033;color:white;border:0;border-radius:12px;padding:12px 20px;font-weight:700;margin-top:10px}pre{white-space:pre-wrap;line-height:1.55}.tag{display:inline-block;background:#eef2ff;padding:6px 10px;border-radius:20px;margin:3px}</style>
<div class='w'><div class='c'><h1>National AI Orchestrator v3.0</h1><p>Multi-Agent · Vector RAG · Document Upload · MCP · Verification · HITL · Audit</p><h3>지식베이스 자료 추가</h3><input id='file' type='file' accept='.pdf,.docx,.txt,.md'><button onclick='upload()'>자료 추가</button><span id='up'></span><hr><h3>질문</h3><textarea id='q'>철도 역세권 개발 시 법령·정책·데이터 관점의 검토사항을 정리해줘</textarea><br><button onclick='go()'>오케스트레이션 실행</button></div><div class='c'><h3>Agent Plan</h3><div id='plan'>대기 중</div><h3>최종 답변</h3><pre id='ans'>질문을 입력하고 실행하세요.</pre><details><summary>근거·검증 Trace 보기</summary><pre id='trace'></pre></details></div></div>
<script>async function upload(){let f=file.files[0];if(!f)return;up.textContent=' 업로드 중...';let d=new FormData();d.append('file',f);let r=await fetch('/knowledge/upload',{method:'POST',body:d});let j=await r.json();up.textContent=r.ok?' '+j.source+' / '+j.chunks+' chunks 저장':' 오류: '+JSON.stringify(j)} async function go(){ans.textContent='분석 중...';plan.textContent='Planning...';try{let r=await fetch('/orchestrate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({user:'analyst',question:q.value})});let j=await r.json();plan.innerHTML=j.plan.map(x=>'<span class=tag>'+x+'</span>').join('');ans.textContent=j.final_answer;trace.textContent=JSON.stringify({rag_context:j.rag_context,verification:j.verification},null,2)}catch(e){ans.textContent='오류: '+e}}</script></html>"""

@app.post("/knowledge/upload")\nasync def knowledge_upload(file:UploadFile=File(...)):\n    suffix=Path(file.filename or "").suffix.lower()\n    if suffix not in {".pdf",".docx",".txt",".md"}: raise HTTPException(400,"PDF, DOCX, TXT, MD만 지원합니다.")\n    with tempfile.NamedTemporaryFile(delete=False,suffix=suffix) as tmp:\n        shutil.copyfileobj(file.file,tmp); p=Path(tmp.name)\n    try:return ingest(p,file.filename or p.name)\n    finally:p.unlink(missing_ok=True)\n\n@app.get("/knowledge")\ndef knowledge(): return stats()\n\n@app.get("/health")
def health(): return {"status":"ok","version":"3.0.0"}
@app.get("/tools")
def tools(): return gateway.list_tools()
@app.post("/orchestrate")
async def run(req:Request): return await orchestrator.run_async(req.user,req.question)
@app.post("/tool/call")
def call_tool(req:ToolRequest):
    meta=next((t for t in gateway.list_tools() if t["name"]==req.tool),None)
    if not meta:return {"status":"denied","reason":"unknown tool"}
    if not allow(req.role,req.tool):return {"status":"denied","reason":"RBAC policy"}
    if requires_human_approval(meta["risk"]):return {"status":"pending_human_approval","tool":req.tool}
    return gateway.call(req.tool,req.payload)
