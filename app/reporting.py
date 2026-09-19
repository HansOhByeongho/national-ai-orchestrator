from datetime import datetime
from pathlib import Path
import json
ROOT=Path("reports")
ROOT.mkdir(exist_ok=True)
def save_report(question,result):
    stamp=datetime.now().strftime("%Y%m%d_%H%M%S")
    p=ROOT/f"orchestration_{stamp}.md"
    sources=sorted(set(x.get("source","unknown") for x in result.get("rag_context",[])))
    body=["# National AI Orchestrator 분석보고서","",f"- 생성시각: {datetime.now().isoformat(timespec='seconds')}",f"- 질문: {question}","","## 최종 분석","",result.get("final_answer",""),"","## 사용 근거"]+[f"- {s}" for s in sources]+["","## Agent",json.dumps(result.get("plan",[]),ensure_ascii=False),"","## Trace",json.dumps(result.get("trace",[]),ensure_ascii=False,indent=2)]
    p.write_text("\n".join(body),encoding="utf-8")
    return str(p)
