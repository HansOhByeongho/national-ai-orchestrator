# National AI Orchestrator v8.2

Public-sector AI orchestration research prototype with evidence-aware multi-agent analysis and configurable live Korean official-data connectors.

## Workflow
Question → hybrid gate/router → uploaded-document RAG → optional evidence reranker → public-data router → MCP / official law & statistics connectors → specialist agents → verifier → uncertainty / human-review check.

## 9 specialist agents
Railway · Urban Development · Legal/Permitting · Finance/Investment · Transport/Demand · GIS/Spatial · Environment/Disaster · Data/Validation · Policy/Administration

## v8.2 integrations
- 21 public-data portal API families are cataloged in `knowledge_catalog/data_go_kr.json`.
- `app/connectors/data_go_router.py` automatically selects relevant datasets from the question and agent domains.
- Hongcheon/Yangdeokwon public demo inputs are stored in `case_studies/hongcheon.json` with 0.5/1/2 km radii.
- `app/routing/jev.py` is an experimental, optional OpenAI-compatible gate/reranker adapter. The adapter name is provisional and does not claim support for a specific vendor/model. If it is not configured, deterministic routing remains active.

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
set JEV_BASE_URL=...
set JEV_API_KEY=...
set JEV_MODEL=...
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
This remains a research prototype. API responses must be interpreted against each provider's official schema and terms. A connector being implemented does not mean a credential has been issued or every dataset is automatically discoverable. data.go.kr datasets have service-specific endpoints and parameters. Current law/statistics should be verified against the returned official source. Do not upload classified, sensitive, personal or unauthorized data. Local knowledge DBs, uploads, reports, logs, .env files and credentials are excluded from Git.
