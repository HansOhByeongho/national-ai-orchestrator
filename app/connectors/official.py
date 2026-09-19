import json,os
from urllib.parse import urlencode
from urllib.request import Request,urlopen

def _get(url,params,timeout=20):
    full=url+"?"+urlencode(params)
    try:
        with urlopen(Request(full,headers={"User-Agent":"NationalAIOrchestrator/6.0"}),timeout=timeout) as r:
            raw=r.read().decode("utf-8","replace")
            try:return {"status":"ok","url":full,"data":json.loads(raw)}
            except Exception:return {"status":"ok","url":full,"text":raw[:20000]}
    except Exception as e:return {"status":"error","url":full,"reason":str(e)}

def law_search(query,display=10):
    oc=os.getenv("LAW_GO_KR_OC")
    if not oc:return {"status":"needs_key","env":"LAW_GO_KR_OC","official":"open.law.go.kr"}
    return _get("https://www.law.go.kr/DRF/lawSearch.do",{"OC":oc,"target":"law","type":"JSON","search":1,"query":query,"display":display})

def law_body(law_id):
    oc=os.getenv("LAW_GO_KR_OC")
    if not oc:return {"status":"needs_key","env":"LAW_GO_KR_OC"}
    return _get("https://www.law.go.kr/DRF/lawService.do",{"OC":oc,"target":"law","type":"JSON","ID":law_id})

def kosis_search(query,count=10):
    key=os.getenv("KOSIS_API_KEY")
    if not key:return {"status":"needs_key","env":"KOSIS_API_KEY","official":"kosis.kr"}
    return _get("https://kosis.kr/openapi/statisticsSearch.do",{"method":"getList","apiKey":key,"searchNm":query,"sort":"RANK","startCount":1,"resultCount":count,"format":"json"})

def kosis_data(params):
    key=os.getenv("KOSIS_API_KEY")
    if not key:return {"status":"needs_key","env":"KOSIS_API_KEY"}
    p=dict(params);p.update({"method":"getList","apiKey":key,"format":"json"})
    return _get("https://kosis.kr/openapi/statisticsData.do",p)

def data_go_get(endpoint,params):
    key=os.getenv("DATA_GO_KR_KEY")
    if not key:return {"status":"needs_key","env":"DATA_GO_KR_KEY","official":"data.go.kr"}
    if not endpoint.startswith("https://apis.data.go.kr/"):return {"status":"denied","reason":"only apis.data.go.kr endpoints are allowed"}
    p=dict(params);p["serviceKey"]=key
    return _get(endpoint,p)

def connector_status():
    return {"law_go_kr":bool(os.getenv("LAW_GO_KR_OC")),"kosis":bool(os.getenv("KOSIS_API_KEY")),"data_go_kr":bool(os.getenv("DATA_GO_KR_KEY")),"implemented":["law_search","law_body","kosis_search","kosis_data","data_go_get"]}
