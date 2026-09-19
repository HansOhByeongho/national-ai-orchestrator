from dataclasses import dataclass

@dataclass
class AgentResult:
    agent: str
    summary: str
    evidence: list[str]

class BaseAgent:
    name = "base"
    keywords: tuple[str, ...] = ()
    def run(self, question: str, context: list[str]) -> AgentResult:
        raise NotImplementedError
