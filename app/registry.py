from app.agents.specialists import PolicyAgent, LegalAgent, DataAgent

class AgentRegistry:
    def __init__(self):
        agents = [PolicyAgent(), LegalAgent(), DataAgent()]
        self.agents = {a.name: a for a in agents}
    def get(self, name): return self.agents[name]
    def all(self): return list(self.agents.values())
