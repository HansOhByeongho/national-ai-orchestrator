DOCUMENTS = ["역세권 개발은 교통·토지이용·산업·주거·관광·재원조달을 함께 검토해야 한다.","공공 AI 시스템은 근거 추적, 접근통제, 사람의 검토와 감사로그를 고려해야 한다.","RAG는 외부 또는 내부 지식에서 관련 근거를 검색하여 생성 과정에 제공하는 방식이다.","MCP는 AI 애플리케이션이 도구와 데이터 소스를 표준화된 방식으로 연결하는 데 활용될 수 있다."]

def retrieve(query: str, k: int = 3) -> list[str]:
    terms = set(query.lower().split())
    ranked = sorted(DOCUMENTS, key=lambda d: sum(t in d.lower() for t in terms), reverse=True)
    return ranked[:k]
