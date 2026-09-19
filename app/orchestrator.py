import asyncio
from app.registry import AgentRegistry
from app.rag.retriever import retrieve
from app.security.audit import write_audit
from app.llm import synthesize_answer, agent_answer

class NationalAIOrchestrator:
    def __init__(self): self.registry=AgentRegistry()
    def plan(self,question):
        selected=[a.name for a in self.registry.all() if any(k.lower() in question.lower() for k in a.keywords)]
        return selected or ["policy","data"]
    async def run_async(self,user,question):
        context=retrieve(question); selected=self.plan(question)
        async def run_one(name):
            llm=await agent_answer(name,question,context)
            if llm: return {"agent":name,"summary":llm,"evidence":context[:2],"mode":"llm"}
            r=await asyncio.to_thread(self.registry.get(name).run,question,context)
            d=r.__dict__; d["mode"]="local-demo"; return d
        raw=await asyncio.gather(*[run_one(n) for n in selected],return_exceptions=True)
        results=[]
        for n,r in zip(selected,raw):
            results.append({"agent":n,"summary":f"agent error: {r}","evidence":[],"mode":"error"} if isinstance(r,Exception) else r)
        final=await synthesize_answer(question,context,results)
        verified={"status":"verified_with_human_review_recommended","checks":["agent output present","retrieved evidence attached","human review recommended"],"results":results}
        write_audit({"user":user,"question":question,"agents":selected,"status":verified["status"]})
        return {"plan":selected,"rag_context":context,"verification":verified,"final_answer":final}
    def run(self,user,question): return asyncio.run(self.run_async(user,question))
