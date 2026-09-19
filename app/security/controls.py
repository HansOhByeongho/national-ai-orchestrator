ROLE_TOOLS = {"analyst": {"policy_search", "legal_search"},"admin": {"policy_search", "legal_search", "write_external"}}
def allow(user_role: str, tool: str) -> bool: return tool in ROLE_TOOLS.get(user_role, set())
def requires_human_approval(risk: str) -> bool: return risk.upper() == "HIGH"
