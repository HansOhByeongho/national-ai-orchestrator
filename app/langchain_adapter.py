"""Optional LangChain/LangGraph portfolio adapter.
The core demo intentionally runs without external LLM credentials.
"""
def integration_points():
    return {"langchain": ["retriever", "tool calling", "prompt/model abstraction"],"langgraph": ["planner node", "agent nodes", "verifier node", "HITL checkpoint"]}
