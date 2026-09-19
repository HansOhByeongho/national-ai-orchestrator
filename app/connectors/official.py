import json, os
from urllib.parse import urlencode
from urllib.request import Request, urlopen
ALLOWLIST=("law.go.kr","kosis.kr","data.go.kr","molit.go.kr","mois.go.kr","me.go.kr","kric.go.kr")
def safe_get_json(url:str,params=None,timeout:int=15):
    if not any(url.startswith("https://"+d) for d in ALLOWLIST):
        return {"status":"denied","reason":"domain not allowlisted"}
    full=url+("?" + urlencode(params) if params else "")
    req=Request(full,headers={"User-Agent":"NationalAIOrchestrator/5.0"})
    try:
        with urlopen(req,timeout=timeout) as r:
            raw=r.read().decode("utf-8","replace")
            try:return {"status":"ok","url":full,"data":json.loads(raw)}
            except Exception:return {"status":"ok","url":full,"text":raw[:12000]}
    except Exception as e:return {"status":"error","url":full,"reason":str(e)}
def connector_status():
    return {"official_domains":list(ALLOWLIST),"data_go_kr_key":bool(os.getenv("DATA_GO_KR_KEY")),"kosis_key":bool(os.getenv("KOSIS_API_KEY")),"note":"API별 URL·파라미터는 해당 기관의 최신 공식 문서에 맞춰 설정해야 합니다."}
