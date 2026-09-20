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


## 오병호 Public AI Toolchain
National AI Orchestrator는 아래 독립 프로젝트를 상위에서 조정하는 방향으로 확장합니다.

- [K-Rail MCP](https://github.com/HansOhByeongho/k-rail-mcp) — 철도·역·교통
- [K-Station AI](https://github.com/HansOhByeongho/k-station-ai) — 역세권 500m·1km·2km 진단
- [K-Urban MCP](https://github.com/HansOhByeongho/k-urban-mcp) — 토지·건축·도시계획
- [K-GIS Agent](https://github.com/HansOhByeongho/k-gis-agent) — 좌표·거리·영향권
- [K-Project Scout](https://github.com/HansOhByeongho/k-project-scout) — 국비·공모·지원사업
- [K-Feasibility](https://github.com/HansOhByeongho/k-feasibility) — 수요·사업비·재원
- [K-Policy Simulator](https://github.com/HansOhByeongho/k-policy-simulator) — 정책 시나리오 비교
- [K-Climate Agent](https://github.com/HansOhByeongho/k-climate-agent) — 탄소·에너지·기후위험
- [K-Public Data MCP](https://github.com/HansOhByeongho/k-public-data-mcp) — 공공데이터 라우팅·게이트웨이

공식 데이터 연계는 공공데이터포털, KOSIS OpenAPI, 국가법령정보 공동활용을 우선하며, 자격증명과 비공개 행정자료는 저장소에 커밋하지 않습니다.
