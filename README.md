# National AI Orchestrator v5.0

Evidence-aware public-sector AI orchestration research prototype.

## Runtime
Question → LangGraph routing → uploaded-document RAG → MCP tools → selected specialist agents → verifier → quality/uncertainty check → human review → audit + Markdown report.

## Specialist agents
Railway, Urban Development, Legal/Permitting, Finance/Investment, Transport/Demand, GIS/Spatial, Environment/Disaster, Data/Validation, Policy/Administration.

## Implemented
- FastAPI web UI and PDF/DOCX/TXT/MD knowledge upload
- persistent chunk store; OpenAI embeddings when configured, keyword fallback otherwise
- executable LangGraph workflow and LangChain ChatOpenAI agents
- MCP Python SDK v2 server/client
- MCP knowledge search, restricted calculator, official-source verification guard, official connector status
- allowlisted official HTTP connector foundation for law.go.kr, KOSIS, data.go.kr, MOLIT, MOIS, ME and KRIC
- evidence source propagation, uncertainty flags, human-review recommendation
- automatic Markdown analysis-report export under reports/
- RBAC/HITL pattern, audit log, Docker and CI

## Run
```cmd
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000

Optional:
```cmd
set OPENAI_API_KEY=YOUR_KEY
set DATA_GO_KR_KEY=YOUR_KEY
set KOSIS_API_KEY=YOUR_KEY
```

## Important boundary
The official connector layer is now executable and domain-allowlisted, but individual Korean government APIs have different endpoints, parameters, authentication and terms. v5 does not pretend that an API is live until its exact endpoint/key is configured and tested. Current law, statistics, program conditions and administrative interpretations must be checked against authoritative sources. Do not upload classified, sensitive, personal, or unauthorized material.

## MCP
The project uses the current MCP Python SDK v2 high-level `MCPServer` and first-class `Client`. Tools expose typed schemas and can be invoked through the MCP client rather than direct function calls.
