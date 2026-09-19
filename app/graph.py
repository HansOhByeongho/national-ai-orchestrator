import asyncio, json, os
from typing import TypedDict, Any
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from app.mcp.client import call_mcp_tool
from app.rag.retriever import retrieve

class OrchestratorState(TypedDict, total=False):
    user:str
    question:str
    plan:list[str]
    rag_context:list[dict]
    mcp_results:dict[str,Any]
    agent_results:list[dict]
    final_answer:str
    trace:list[str]

def select_agents(question:str)->list[str]:
    q=question.lower(); out=[]
    if any(k in q for k in ("정책","사업","계획","행정","지역개발")): out.append("policy")
    if any(k in q for k in ("법","법령","규제","인허가","조례")): out.append("legal")
    if any(k in q for k in ("데이터","통계","수요","분석","예측")): out.append("data")
    return out or ["policy","data"]

async def planner(state):
    return {"plan":select_agents(state["question"]),"trace":["LangGraph: planner"]}

async def retrieval(state):
    ctx=retrieve(state["question"])
    return {"rag_context":ctx,"trace":state.get("trace",[])+["LangGraph: RAG retrieval"]}

async def tools(state):
    mapping={"policy":"policy_search","legal":"legal_search","data":"data_search"}
    calls=await asyncio.gather(*[call_mcp_tool(mapping[a],state["question"]) for a in state["plan"]])
    return {"mcp_results":dict(zip(state["plan"],calls)),"trace":state.get("trace",[])+["MCP v2 Client → MCPServer tools/call"]}

async def specialists(state):
    key=os.getenv("OPENAI_API_KEY"); results=[]
    roles={"policy":"공공정책 분석가","legal":"법·규제 검토 에이전트","data":"데이터 분석가"}
    if key:
        model=ChatOpenAI(model=os.getenv("OPENAI_MODEL","gpt-5-mini"),temperature=0)
        async def one(a):
            prompt=f"""역할: {roles[a]}
질문: {state['question']}
RAG 근거(출처 포함): {json.dumps(state['rag_context'],ensure_ascii=False)}
MCP 도구 결과: {json.dumps(state['mcp_results'].get(a,{}),ensure_ascii=False)}
근거와 일반 분석을 구분하고 확인되지 않은 법령·수치를 만들지 말라. 한국어로 핵심 분석을 작성하라."""
            msg=await model.ainvoke(prompt)
            return {"agent":a,"summary":str(msg.content),"mode":"LangChain ChatOpenAI + MCP"}
        results=await asyncio.gather(*[one(a) for a in state["plan"]])
    else:
        for a in state["plan"]:
            results.append({"agent":a,"summary":f"{roles[a]} 로컬 데모. MCP 결과: {state['mcp_results'].get(a,{})}","mode":"LangGraph + MCP local-demo"})
    return {"agent_results":results,"trace":state.get("trace",[])+["LangChain specialist agents"]}

async def verifier(state):
    if os.getenv("OPENAI_API_KEY"):
        model=ChatOpenAI(model=os.getenv("OPENAI_MODEL","gpt-5-mini"),temperature=0)
        prompt=f"""당신은 National AI Orchestrator의 Verifier다.
질문: {state['question']}
RAG(출처 포함): {json.dumps(state['rag_context'],ensure_ascii=False)}
MCP: {json.dumps(state['mcp_results'],ensure_ascii=False)}
Agent 결과: {json.dumps(state['agent_results'],ensure_ascii=False)}
중복·충돌을 정리하고 근거/추가확인을 구분하여 실행순서가 있는 한국어 최종보고서를 작성하라."""
        msg=await model.ainvoke(prompt); answer=str(msg.content)
    else:
        answer="[로컬 데모 모드]\n"+ "\n".join(f"• {r['agent'].upper()}: {r['summary']}" for r in state["agent_results"])
    return {"final_answer":answer,"trace":state.get("trace",[])+["LangGraph: verifier → END"]}

builder=StateGraph(OrchestratorState)
builder.add_node("planner",planner)
builder.add_node("retrieval",retrieval)
builder.add_node("mcp_tools",tools)
builder.add_node("specialists",specialists)
builder.add_node("verifier",verifier)
builder.add_edge(START,"planner")
builder.add_edge("planner","retrieval")
builder.add_edge("retrieval","mcp_tools")
builder.add_edge("mcp_tools","specialists")
builder.add_edge("specialists","verifier")
builder.add_edge("verifier",END)
orchestration_graph=builder.compile()

async def run_graph(user:str,question:str)->dict:
    return await orchestration_graph.ainvoke({"user":user,"question":question,"trace":[]})
