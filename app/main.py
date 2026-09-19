from fastapi import FastAPI
from pydantic import BaseModel, Field
from app.orchestrator import NationalAIOrchestrator
from app.mcp.gateway import MCPGateway
from app.security.controls import allow, requires_human_approval

app = FastAPI(title="National AI Orchestrator v1.0", version="1.0.0")
orchestrator = NationalAIOrchestrator()
gateway = MCPGateway()

class Request(BaseModel):
    user: str = "analyst"
    question: str = Field(min_length=3)

class ToolRequest(BaseModel):
    role: str = "analyst"
    tool: str
    payload: dict = {}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/tools")
def tools():
    return gateway.list_tools()

@app.post("/orchestrate")
def run(req: Request):
    return orchestrator.run(req.user, req.question)

@app.post("/tool/call")
def call_tool(req: ToolRequest):
    tool_meta = next((t for t in gateway.list_tools() if t["name"] == req.tool), None)
    if not tool_meta:
        return {"status": "denied", "reason": "unknown tool"}
    if not allow(req.role, req.tool):
        return {"status": "denied", "reason": "RBAC policy"}
    if requires_human_approval(tool_meta["risk"]):
        return {"status": "pending_human_approval", "tool": req.tool}
    return gateway.call(req.tool, req.payload)
