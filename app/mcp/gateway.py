from app.mcp.tools import TOOLS

class MCPGateway:
    """Portfolio implementation of an MCP-style policy enforcement gateway."""
    def list_tools(self): return [{"name": t.name, "description": t.description, "risk": t.risk} for t in TOOLS.values()]
    def call(self, name: str, payload: dict):
        if name not in TOOLS: raise KeyError(f"Unknown tool: {name}")
        return TOOLS[name].execute(payload)
