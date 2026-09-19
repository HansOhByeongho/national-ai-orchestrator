import asyncio,json,os
from typing import TypedDict,Any
from langgraph.graph import StateGraph,START,END
from langchain_openai import ChatOpenAI
from app.mcp.client import call_mcp_tool
from app.rag.retriever import retrieve
from app.agent_catalog import AGENTS,select
from app.verification import evidence_coverage

class State(TypedDict,total=False):
 user:str; question:str; plan:list[str]; rag_context:list[dict]; mcp_results:dict[str,Any]; agent_results:list[dict]; final_answer:str; trace:list[str]; quality:dict

async def planner(s):
 return {"plan":select(s["question"]),"trace":["planner: domain routing"]}

async def retrieval(s):
 ctx=retrieve(s["question"],8)
 return {"rag_context":ctx,"trace":s.get("trace",[])+[f"rag: {len(ctx)} evidence chunks"]}

async def tools(s):
 kb=await call_mcp_tool("knowledge_search",{"query":s["question"],"limit":8})
 guard=await call_mcp_tool("official_source_check",{"topic":s["question"]})
 return {"mcp_results":{"knowledge":kb,"official_source_guard":guard},"trace":s.get("trace",[])+["mcp: knowledge_search + official_source_check"]}

async def specialists(s):
 results=[]
 if os.getenv("OPENAI_API_KEY"):
  model=ChatOpenAI(model=os.getenv("OPENAI_MODEL","gpt-5-mini"),temperature=0)
  async def one(a):
   p=f"""역할: {AGENTS[a]['role']}
질문: {s['question']}
검색 근거: {json.dumps(s['rag_context'],ensure_ascii=False)}
MCP 결과: {json.dumps(s['mcp_results'],ensure_ascii=False)}
규칙: 1) 업로드 근거와 일반 분석을 구분 2) 출처 파일명을 괄호로 표시 3) 없는 법령·수치 생성 금지 4) 확인 필요사항 명시 5) 실무 검토항목과 다음 행동을 구체화. 한국어로 상세 분석."""
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
  p=f"""당신은 최종 Verifier다. 질문={s['question']}
근거={json.dumps(s['rag_context'],ensure_ascii=False)}
전문가 결과={json.dumps(s['agent_results'],ensure_ascii=False)}
최종보고서를 ①핵심결론 ②분야별 분석 ③근거와 출처 ④쟁점·충돌·불확실성 ⑤실행순서 ⑥추가확인자료 순으로 작성하라. 업로드 자료에 없는 최신 법령·수치·사실은 단정하지 말고 공식 원문 확인 필요라고 표시하라."""
  msg=await model.ainvoke(p); ans=str(msg.content)
 else:
  ans="[로컬 데모 모드]\n"+"\n".join(f"■ {r['label']}\n{r['summary']}" for r in s["agent_results"])
 quality=evidence_coverage(ans,s["rag_context"])
 return {"final_answer":ans,"quality":quality,"trace":s.get("trace",[])+["verifier: evidence/uncertainty check","END"]}

b=StateGraph(State)
for n,f in [("planner",planner),("retrieval",retrieval),("mcp_tools",tools),("specialists",specialists),("verifier",verifier)]:b.add_node(n,f)
b.add_edge(START,"planner");b.add_edge("planner","retrieval");b.add_edge("retrieval","mcp_tools");b.add_edge("mcp_tools","specialists");b.add_edge("specialists","verifier");b.add_edge("verifier",END)
graph=b.compile()
async def run_graph(user,question):return await graph.ainvoke({"user":user,"question":question,"trace":[]})
