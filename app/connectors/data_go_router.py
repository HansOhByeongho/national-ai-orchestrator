import re
from app.connectors.data_go_catalog import datasets

DOMAIN_TERMS={
 "railway":["철도","열차","역","역사","광역철도"],
 "transport":["교통","통행","환승","수요","od","버스","도로","cctv"],
 "gis":["gis","공간","반경","거리","입지","poi","주변"],
 "urban":["역세권","도시개발","개발","토지","건축","주택","아파트","용도지역"],
 "legal":["법","인허가","규제","법령"],
 "finance":["사업비","재정","투자","지가","공시지가","실거래","지원사업"],
 "policy":["정책","공모","지원","관광"],
 "data":["통계","데이터","인구","방문자"]
}
def route(question,plan=None,limit=8):
 q=question.lower(); wanted=set(plan or [])
 for domain,terms in DOMAIN_TERMS.items():
  if any(t in q for t in terms): wanted.add(domain)
 scored=[]
 for d in datasets():
  overlap=len(wanted.intersection(d.get("agents",[])))
  title_hits=sum(1 for t in re.findall(r"[가-힣A-Za-z0-9]+",q) if len(t)>=2 and t.lower() in d.get("title","").lower())
  score=overlap*10+title_hits
  if score: scored.append((score,d))
 scored.sort(key=lambda x:(-x[0],x[1]["id"]))
 return [dict(x[1],route_score=x[0]) for x in scored[:limit]]

def executable_routes(question,plan=None,limit=8):
 return [d for d in route(question,plan,limit) if d.get("enabled") and d.get("endpoint")]
