from mcp.server import MCPServer
from app.rag.store import search, stats
mcp=MCPServer("National AI Orchestrator Tools")

@mcp.tool()
def knowledge_search(query:str, limit:int=6)->dict:
    """Search the user-authorized local knowledge base."""
    return {"query":query,"results":search(query,max(1,min(limit,12)))}

@mcp.tool()
def knowledge_stats()->dict:
    """Return knowledge-base source and chunk counts."""
    return stats()

@mcp.tool()
def calculation(expression:str)->dict:
    """Evaluate a basic arithmetic expression with a restricted character set."""
    import re
    if not re.fullmatch(r"[0-9+\-*/(). %]+",expression): return {"status":"denied","reason":"unsupported expression"}
    try:return {"expression":expression,"result":eval(expression,{"__builtins__":{}},{})}
    except Exception as e:return {"status":"error","reason":str(e)}

@mcp.tool()
def official_source_check(topic:str)->dict:
    """Return a guardrail for facts that require authoritative external verification."""
    return {"topic":topic,"status":"external_verification_required","guidance":"최신 법령·정부계획·통계·공모조건은 해당 공식 원문/API에서 재확인하십시오."}
