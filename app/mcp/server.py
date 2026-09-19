from mcp.server import MCPServer

mcp = MCPServer("National AI Orchestrator Tools")

@mcp.tool()
def policy_search(query: str) -> dict:
    """Search the authorized demo policy knowledge base."""
    docs=[
      "역세권 개발은 교통·토지이용·산업·주거·관광·재원조달을 함께 검토해야 한다.",
      "공공 AI 시스템은 근거 추적, 접근통제, 사람의 검토와 감사로그를 고려해야 한다."
    ]
    return {"query":query,"results":docs}

@mcp.tool()
def legal_search(query: str) -> dict:
    """Return legal-review guardrails from the authorized demo knowledge base."""
    return {"query":query,"results":["법령명·조문·인허가 요건은 최신 공식 원문으로 재확인해야 한다.","확인되지 않은 법률·수치·사실을 생성하지 않는다."]}

@mcp.tool()
def data_search(query: str) -> dict:
    """Return data-analysis requirements from the authorized demo knowledge base."""
    return {"query":query,"results":["수요·인구·교통·토지·사업비 데이터의 기준시점과 출처를 함께 관리한다.","비교지표와 검증방법을 사전에 정의한다."]}
