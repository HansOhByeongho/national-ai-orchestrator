import re
def evidence_coverage(answer:str, evidence:list[dict])->dict:
    sources=sorted(set(x.get("source","unknown") for x in evidence))
    uncertainty=len(re.findall(r"확인 필요|재확인|추가 확인|불확실",answer))
    return {"sources":sources,"source_count":len(sources),"uncertainty_flags":uncertainty,"human_review_required":True}
