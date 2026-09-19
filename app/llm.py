import os, json, asyncio
from urllib.request import Request, urlopen

def _call_openai(prompt: str) -> str:
    key=os.getenv("OPENAI_API_KEY")
    if not key: return ""
    body=json.dumps({"model":os.getenv("OPENAI_MODEL","gpt-5-mini"),"input":prompt}).encode("utf-8")
    req=Request("https://api.openai.com/v1/responses",data=body,headers={"Authorization":f"Bearer {key}","Content-Type":"application/json"})
    with urlopen(req,timeout=60) as res: data=json.loads(res.read())
    for item in data.get("output",[]):
        for part in item.get("content",[]):
            if part.get("type")=="output_text": return part.get("text","")
    return ""

async def agent_answer(agent, question, context):
    if not os.getenv("OPENAI_API_KEY"): return None
    roles={
      "policy":"정책분석가. 정책목표, 이해관계자, 추진절차, 정책수단과 리스크를 분석한다.",
      "legal":"법·규제 검토 에이전트. 제공된 근거 범위 안에서 관련 법률·인허가 검토사항과 추가 확인사항을 구분한다. 법령을 임의로 만들어내지 않는다.",
      "data":"데이터분석가. 필요한 데이터, 지표, 수요예측, 비교기준과 검증방법을 제시한다."
    }
    prompt=f"""역할: {roles.get(agent,agent)}
사용자 질문: {question}
RAG 검색근거: {json.dumps(context,ensure_ascii=False)}
검색근거와 일반적 분석을 명확히 구분하고, 확인되지 않은 사실은 확인 필요라고 표시하라. 한국어로 5~8개 핵심사항을 작성하라."""
    try:return await asyncio.to_thread(_call_openai,prompt)
    except Exception as e:return f"Agent LLM 오류: {e}"

async def synthesize_answer(question, context, results):
    if not os.getenv("OPENAI_API_KEY"):
        lines=["[로컬 데모 모드] OPENAI_API_KEY를 설정하면 각 Agent와 최종 종합 단계에서 실제 LLM을 호출합니다.","",f"질문: {question}",""]
        for r in results: lines.append(f"• {r['agent'].upper()}: {r['summary']}")
        lines += ["","RAG 근거:"]+[f"- {x}" for x in context]
        return "\n".join(lines)
    prompt=f"""당신은 공공부문 National AI Orchestrator의 Verifier 겸 최종 종합 에이전트다.
질문: {question}
RAG 근거: {json.dumps(context,ensure_ascii=False)}
전문 Agent 결과: {json.dumps(results,ensure_ascii=False)}
요구사항:
1. Agent 간 중복·충돌을 정리한다.
2. 근거가 있는 내용과 추가 확인이 필요한 내용을 구분한다.
3. 정책/법률/데이터 관점의 실행 가능한 검토 순서를 제시한다.
4. 제공되지 않은 법령명·수치·사실을 만들어내지 않는다.
5. 한국어 보고서 형식으로 답한다."""
    try:
        answer=await asyncio.to_thread(_call_openai,prompt)
        return answer or "LLM 응답을 해석하지 못했습니다."
    except Exception as e:return f"LLM 호출 오류: {e}"
