import asyncio,json,os
from typing import TypedDict,Any
from langgraph.graph import StateGraph,START,END
from langchain_openai import ChatOpenAI
from app.mcp.client import call_mcp_tool
from app.rag.retriever import retrieve
from app.agent_catalog import AGENTS,select
from app.verification import evidence_coverage
from app.connectors.data_go_router import route as route_public_data

class State(TypedDict,total=False):
    user:str
    question:str
    plan:list[str]
    rag_context:list[dict]
    mcp_results:dict[str,Any]
    agent_results:list[dict]
    final_answer:str
    trace:list[str]
    quality:dict

async def planner(s):
    return {"plan":select(s["question"]),"trace":["planner: domain routing"]}

async def retrieval(s):
    ctx=retrieve(s["question"],8)
    return {"rag_context":ctx,"trace":s.get("trace",[])+[f"rag: {len(ctx)} evidence chunks"]}

async def tools(s):
    kb=await call_mcp_tool("knowledge_search",{"query":s["question"],"limit":8})
    connector=await call_mcp_tool("official_connector_status",{})
    official={}
    public_data_routes=route_public_data(s["question"],s["plan"],8)
    if "legal" in s["plan"] and connector.get("law_go_kr"):
        official["law"]=await call_mcp_tool("korean_law_search",{"query":s["question"],"display":5})
    if ("data" in s["plan"] or "transport" in s["plan"]) and connector.get("kosis"):
        official["kosis"]=await call_mcp_tool("kosis_statistics_search",{"query":s["question"],"count":5})
    return {"mcp_results":{"knowledge":kb,"official_connectors":connector,"official_results":official,"public_data_routes":public_data_routes},"trace":s.get("trace",[])+[f"public-data router: {len(public_data_routes)} candidates","mcp: knowledge + configured official connectors"]}

async def specialists(s):
    results=[]
    if os.getenv("OPENAI_API_KEY"):
        model=ChatOpenAI(model=os.getenv("OPENAI_MODEL","gpt-5-mini"),temperature=0)
        async def one(a):
            p=f"""역할: {AGENTS[a]['role']}
질문: {s['question']}
검색 근거: {json.dumps(s['rag_context'],ensure_ascii=False)}
MCP 결과: {json.dumps(s['mcp_results'],ensure_ascii=False)}
규칙: 업로드 근거와 일반 분석을 구분하고, 출처 파일명을 표시하며, 확인되지 않은 법령·수치를 만들지 말고, 확인 필요사항과 다음 행동을 구체적으로 작성하라."""
            msg=await model.ainvoke(p)
            return {"agent":a,"label":AGENTS[a]["label"],"summary":str(msg.content),"mode":"LangChain LLM"}
        results=await asyncio.gather(*[one(a) for a in s["plan"]])
    else:
        for a in s["plan"]:
            results.append({"agent":a,"label":AGENTS[a]["label"],"summary":f"{AGENTS[a]['role']} 현재 API 키가 없어 검색 근거 중심의 로컬 데모로 실행했습니다.","mode":"local-demo"})
    return {"agent_results":results,"trace":s.get("trace",[])+[f"agents: {len(results)} specialists"]}

async def verifier(s):
    if os.getenv("OPENAI_API_KEY"):
        model=ChatOpenAI(model=os.getenv("OPENAI_MODEL","gpt-5-mini"),temperature=0)
        p=f"""당신은 최종 Verifier다.
질문: {s['question']}
근거: {json.dumps(s['rag_context'],ensure_ascii=False)}
전문가 결과: {json.dumps(s['agent_results'],ensure_ascii=False)}
최종보고서를 핵심결론, 분야별 분석, 근거와 출처, 쟁점·불확실성, 실행순서, 추가확인자료 순으로 작성하라."""
        msg=await model.ainvoke(p)
        ans=str(msg.content)
    else:
        ans="[로컬 데모 모드]\n"+"\n".join(f"■ {r['label']}\n{r['summary']}" for r in s["agent_results"])
    quality=evidence_coverage(ans,s["rag_context"])
    return {"final_answer":ans,"quality":quality,"trace":s.get("trace",[])+["verifier: evidence/uncertainty check","END"]}

b=StateGraph(State)
for n,f in [("planner",planner),("retrieval",retrieval),("mcp_tools",tools),("specialists",specialists),("verifier",verifier)]:
    b.add_node(n,f)
b.add_edge(START,"planner")
b.add_edge("planner","retrieval")
b.add_edge("retrieval","mcp_tools")
b.add_edge("mcp_tools","specialists")
b.add_edge("specialists","verifier")
b.add_edge("verifier",END)
graph=b.compile()

async def run_graph(user,question):
    return await graph.ainvoke({"user":user,"question":question,"trace":[]})
