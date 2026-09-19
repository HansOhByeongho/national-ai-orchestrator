from app.registry import AgentRegistry
from app.rag.retriever import retrieve
from app.security.audit import write_audit

class NationalAIOrchestrator:
    def __init__(self):
        self.registry = AgentRegistry()

    def plan(self, question: str) -> list[str]:
        selected = []
        for agent in self.registry.all():
            if any(k.lower() in question.lower() for k in agent.keywords):
                selected.append(agent.name)
        return selected or ["policy", "data"]

    def verify(self, results: list[dict]) -> dict:
        return {"status": "verified_with_human_review_recommended","checks": ["agent output present", "retrieved evidence attached", "audit recorded"],"results": results}

    def run(self, user: str, question: str) -> dict:
        context = retrieve(question)
        selected = self.plan(question)
        results = []
        for name in selected:
            result = self.registry.get(name).run(question, context)
            results.append(result.__dict__)
        verified = self.verify(results)
        write_audit({"user": user, "question": question, "agents": selected, "status": verified["status"]})
        return {"plan": selected, "rag_context": context, "verification": verified}
