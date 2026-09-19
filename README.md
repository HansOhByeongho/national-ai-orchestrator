# National AI Orchestrator v4.0

Evidence-aware public-sector AI orchestration research prototype.

> This repository demonstrates current technical capability and research/development output. It does **not** claim historical employment duration, production deployment, or autonomous legal authority.

## What makes this orchestration
A single question is routed through a LangGraph workflow: **domain routing → document RAG → MCP tools → specialist agents → evidence-aware verifier → audit**.

### Specialist agents
Railway · Urban Development · Legal/Permitting · Finance/Investment · Transport/Demand · GIS/Spatial · Environment/Disaster · Data/Validation · Policy/Administration.

### Implemented capabilities
- FastAPI web application and upload UI
- LangGraph executable state workflow
- LangChain `ChatOpenAI` specialist execution when `OPENAI_API_KEY` is configured
- Official MCP Python SDK v2 server/client with knowledge-search, calculation and official-source-check tools
- PDF/DOCX/TXT/MD ingestion, chunking and persistent local knowledge store
- OpenAI embeddings semantic retrieval when an API key is configured; keyword fallback otherwise
- Source-aware evidence passed to specialists and final verifier
- Evidence coverage / uncertainty flags and human-review recommendation
- RBAC/HITL pattern and audit log
- Docker and GitHub Actions tests

## Run
```bash
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```
Open `http://127.0.0.1:8000`.

Optional LLM + semantic embeddings:
```cmd
set OPENAI_API_KEY=YOUR_KEY
python -m uvicorn app.main:app --reload
```

## Knowledge base
Upload PDF, DOCX, TXT or Markdown in the web UI. Files are parsed locally into chunks and persisted to `data/knowledge.json`. With an API key, embeddings are stored for semantic retrieval. Do not upload classified, sensitive, personal, or otherwise unauthorized material.

## Architecture
```text
User
  ↓
LangGraph Planner / Domain Router
  ↓
Vector/Keyword RAG ── MCP Knowledge Tools
  ↓
Specialist Agents (selected by task)
  ↓
Verifier / Evidence & Uncertainty Check
  ↓
Human Review + Audit
```

## Important limitations
This is a research prototype. The `official_source_check` tool is a guardrail, not a live government-law/statistics connector. Current statutes, official statistics and program conditions must be verified against authoritative sources. GIS computation and external government APIs are not yet live integrations. Uploaded PDF extraction depends on embedded text; scanned PDFs require OCR preprocessing.
