from app.graph import run_graph
from app.security.audit import write_audit
class NationalAIOrchestrator:
 async def run_async(self,user,question):
  s=await run_graph(user,question)
  verification={"status":"human_review_recommended","quality":s.get("quality",{}),"results":s.get("agent_results",[])}
  write_audit({"user":user,"question":question,"agents":s.get("plan",[]),"status":verification["status"]})
  return {"plan":s.get("plan",[]),"rag_context":s.get("rag_context",[]),"mcp_results":s.get("mcp_results",{}),"verification":verification,"trace":s.get("trace",[]),"final_answer":s.get("final_answer","")}
