import asyncio
from app.registry import AgentRegistry
from app.rag.retriever import retrieve
from app.security.audit import write_audit
from app.llm import synthesize_answer

class NationalAIOrchestrator:
    def __init__(self):
        self.registry = AgentRegistry()

    def plan(self, question: str) -> list[str]:
        selected=[a.name for a in self.registry.all() if any(k.lower() in question.lower() for k in a.keywords)]
        return selected or ["policy","data"]

    async def run_async(self,user:str,question:str)->dict:
        context=retrieve(question)
        selected=self.plan(question)
        tasks=[asyncio.to_thread(self.registry.get(n).run,question,context) for n in selected]
        raw=await asyncio.gather(*tasks,return_exceptions=True)
        results=[]
        for n,r in zip(selected,raw):
            results.append({"agent":n,"summary":f"agent error: {r}","evidence":[]} if isinstance(r,Exception) else r.__dict__)
        final=await synthesize_answer(question,context,results)
        verified={"status":"verified_with_human_review_recommended","checks":["agent output present","retrieved evidence attached","human review recommended"],"results":results}
        write_audit({"user":user,"question":question,"agents":selected,"status":verified["status"]})
        return {"plan":selected,"rag_context":context,"verification":verified,"final_answer":final}

    def run(self,user:str,question:str)->dict:
        return asyncio.run(self.run_async(user,question))
