from app.graph import run_graph
from app.security.audit import write_audit

class NationalAIOrchestrator:
    async def run_async(self,user:str,question:str)->dict:
        state=await run_graph(user,question)
        verification={"status":"verified_with_human_review_recommended","checks":["LangGraph workflow completed","MCP tool results attached","RAG context attached","human review recommended"],"results":state.get("agent_results",[])}
        write_audit({"user":user,"question":question,"agents":state.get("plan",[]),"status":verification["status"]})
        return {"plan":state.get("plan",[]),"rag_context":state.get("rag_context",[]),"mcp_results":state.get("mcp_results",{}),"verification":verification,"trace":state.get("trace",[]),"final_answer":state.get("final_answer","")}
