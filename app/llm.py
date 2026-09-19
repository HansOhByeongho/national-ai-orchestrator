import os, json, asyncio
from urllib.request import Request, urlopen

async def synthesize_answer(question, context, results):
    key=os.getenv("OPENAI_API_KEY")
    if not key:
        lines=["[로컬 데모 모드] 실제 LLM을 사용하려면 OPENAI_API_KEY를 설정하세요.","",f"질문: {question}",""]
        for r in results: lines.append(f"• {r['agent'].upper()}: {r['summary']}")
        lines += ["","근거:"]+[f"- {x}" for x in context]
        return "\n".join(lines)
    prompt=f"""당신은 공공부문 AI 오케스트레이터의 최종 검증·종합 에이전트다.
질문: {question}
검색 근거: {json.dumps(context,ensure_ascii=False)}
전문 에이전트 결과: {json.dumps(results,ensure_ascii=False)}
근거와 에이전트 결과를 구분하고, 과장하지 말며, 한국어로 구조화된 최종 답변을 작성하라."""
    def call():
        body=json.dumps({"model":os.getenv("OPENAI_MODEL","gpt-5-mini"),"input":prompt}).encode()
        req=Request("https://api.openai.com/v1/responses",data=body,headers={"Authorization":f"Bearer {key}","Content-Type":"application/json"})
        with urlopen(req,timeout=60) as res:
            data=json.loads(res.read())
        for item in data.get("output",[]):
            for part in item.get("content",[]):
                if part.get("type")=="output_text": return part.get("text","")
        return "LLM 응답을 해석하지 못했습니다."
    try:return await asyncio.to_thread(call)
    except Exception as e:return f"LLM 호출 오류: {e}"
