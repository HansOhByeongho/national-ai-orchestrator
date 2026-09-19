from app.rag.store import search
FALLBACK=[
 {"source":"built-in","chunk":0,"text":"역세권 개발은 교통·토지이용·산업·주거·관광·재원조달을 함께 검토해야 한다."},
 {"source":"built-in","chunk":1,"text":"공공 AI 시스템은 근거 추적, 접근통제, 사람의 검토와 감사로그를 고려해야 한다."},
 {"source":"built-in","chunk":2,"text":"MCP는 AI 애플리케이션이 도구와 데이터 소스를 표준화된 방식으로 연결하는 데 활용될 수 있다."}
]
def retrieve(query:str,k:int=6):
    found=search(query,k)
    return found or FALLBACK[:k]
