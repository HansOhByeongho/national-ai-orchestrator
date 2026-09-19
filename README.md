# National AI Orchestrator v6.0

Public-sector AI orchestration research prototype with evidence-aware multi-agent analysis and configurable live Korean official-data connectors.

## Workflow
Question → LangGraph router → uploaded-document RAG → MCP → official law/statistics tools when configured → specialist agents → verifier → uncertainty check → human review → audit/report.

## 9 specialist agents
Railway · Urban Development · Legal/Permitting · Finance/Investment · Transport/Demand · GIS/Spatial · Environment/Disaster · Data/Validation · Policy/Administration

## Live connector implementations
- National Law Information: statute search and statute-body retrieval
- KOSIS: integrated statistics search and statistics-data retrieval
- data.go.kr: generic approved `https://apis.data.go.kr/` endpoint caller
- All connectors fail closed with `needs_key` when credentials are absent.

Environment variables:
```cmd
set OPENAI_API_KEY=...
set LAW_GO_KR_OC=...
set KOSIS_API_KEY=...
set DATA_GO_KR_KEY=...
```

## Run
```cmd
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000

## Knowledge
PDF/DOCX/TXT/MD uploads are chunked and persisted. With OpenAI configured, semantic embeddings are used; otherwise keyword retrieval is used.

## MCP tools
`knowledge_search`, `knowledge_stats`, `calculation`, `official_connector_status`, `korean_law_search`, `korean_law_body`, `kosis_statistics_search`, `kosis_statistics_data`, `public_data_get`.

## Safety / accuracy
This remains a research prototype. API responses must be interpreted against each provider's official schema and terms. A connector being implemented does not mean a credential has been issued or every dataset is automatically discoverable. data.go.kr datasets have service-specific endpoints and parameters. Current law/statistics should be verified against the returned official source. Do not upload classified, sensitive, personal or unauthorized data.
