from mcp.server import MCPServer
from app.rag.store import search,stats
from app.connectors.official import connector_status,law_search,law_body,kosis_search,kosis_data,data_go_get
mcp=MCPServer("National AI Orchestrator Tools")
@mcp.tool()
def knowledge_search(query:str,limit:int=8)->dict:return {"query":query,"results":search(query,max(1,min(limit,16)))}
@mcp.tool()
def knowledge_stats()->dict:return stats()
@mcp.tool()
def calculation(expression:str)->dict:
 import re
 if not re.fullmatch(r"[0-9+\-*/(). %]+",expression):return {"status":"denied","reason":"unsupported expression"}
 try:return {"expression":expression,"result":eval(expression,{"__builtins__":{}},{})}
 except Exception as e:return {"status":"error","reason":str(e)}
@mcp.tool()
def official_connector_status()->dict:return connector_status()
@mcp.tool()
def korean_law_search(query:str,display:int=10)->dict:
 """Search current Korean statutes through the official National Law Information API."""
 return law_search(query,display)
@mcp.tool()
def korean_law_body(law_id:str)->dict:
 """Retrieve a statute body by official law ID."""
 return law_body(law_id)
@mcp.tool()
def kosis_statistics_search(query:str,count:int=10)->dict:
 """Search KOSIS official statistical tables."""
 return kosis_search(query,count)
@mcp.tool()
def kosis_statistics_data(params:dict)->dict:
 """Retrieve KOSIS statistical data using official API parameters."""
 return kosis_data(params)
@mcp.tool()
def public_data_get(endpoint:str,params:dict)->dict:
 """Call an approved apis.data.go.kr endpoint with the configured service key."""
 return data_go_get(endpoint,params)
