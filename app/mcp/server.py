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

from app.analytics.spatial import haversine_km,influence_zone
from app.analytics.finance import development_cost,funding_mix
from app.analytics.demand import scenario_demand

@mcp.tool()
def geo_distance_km(lat1:float,lon1:float,lat2:float,lon2:float)->dict:
 """Calculate great-circle distance between two coordinates."""
 return {"distance_km":round(haversine_km(lat1,lon1,lat2,lon2),3)}

@mcp.tool()
def geo_influence_zone(lat:float,lon:float,points:list[dict],radius_km:float=2.0)->dict:
 """Measure points against a station-centered influence radius."""
 return influence_zone(lat,lon,points,radius_km)

@mcp.tool()
def estimate_development_cost(area_m2:float,unit_cost_per_m2:float,contingency_pct:float=10)->dict:
 """Transparent arithmetic development-cost scenario."""
 return development_cost(area_m2,unit_cost_per_m2,contingency_pct)

@mcp.tool()
def estimate_funding_mix(total:float,shares:dict)->dict:
 """Split a total project cost by user-supplied funding shares."""
 return funding_mix(total,shares)

@mcp.tool()
def estimate_demand_scenario(base_population:float,trip_rate:float,capture_rate:float,rail_share:float)->dict:
 """Simple auditable scenario model; not an official transport forecast."""
 return scenario_demand(base_population,trip_rate,capture_rate,rail_share)
