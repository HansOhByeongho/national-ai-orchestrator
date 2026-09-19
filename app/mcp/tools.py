from dataclasses import dataclass

@dataclass
class Tool:
    name: str
    description: str
    risk: str = "LOW"
    def execute(self, payload: dict) -> dict: return {"tool": self.name, "status": "ok", "payload": payload}

TOOLS = {"policy_search": Tool("policy_search", "Search authorized policy knowledge"),"legal_search": Tool("legal_search", "Search authorized legal knowledge"),"write_external": Tool("write_external", "Example high-risk external write action", "HIGH")}
