from mcp.server import MCPServer
from app.rag.store import search,stats
from app.connectors.official import connector_status,safe_get_json
mcp=MCPServer("National AI Orchestrator Tools")
@mcp.tool()
def knowledge_search(query:str,limit:int=8)->dict:
    """Search user-authorized local evidence."""
    return {"query":query,"results":search(query,max(1,min(limit,16)))}
@mcp.tool()
def knowledge_stats()->dict:
    """Return knowledge-base status."""
    return stats()
@mcp.tool()
def calculation(expression:str)->dict:
    """Evaluate restricted arithmetic only."""
    import re
    if not re.fullmatch(r"[0-9+\-*/(). %]+",expression):return {"status":"denied","reason":"unsupported expression"}
    try:return {"expression":expression,"result":eval(expression,{"__builtins__":{}},{})}
    except Exception as e:return {"status":"error","reason":str(e)}
@mcp.tool()
def official_connector_status()->dict:
    """Show configured official-source connector capability."""
    return connector_status()
@mcp.tool()
def official_http_get(url:str,params:dict|None=None)->dict:
    """GET only from explicitly allowlisted Korean official domains. Use only known official API endpoints."""
    return safe_get_json(url,params)
@mcp.tool()
def official_source_check(topic:str)->dict:
    """Mark time-sensitive legal/statistical claims for authoritative verification."""
    return {"topic":topic,"status":"external_verification_required","preferred_domains":["law.go.kr","kosis.kr","data.go.kr","molit.go.kr"],"guidance":"최신 법령·통계·공모조건은 공식 원문/API로 재확인"}
