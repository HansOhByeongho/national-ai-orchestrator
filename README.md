# National AI Orchestrator v2.0

Research prototype for public-sector AI orchestration using **AI Agents, RAG, MCP-style tools, multi-agent routing, verification, HITL, audit logging, Docker, and CI**.

> This repository demonstrates current technical capability and research/development output. It does **not** claim historical employment duration.

## Recruitment-relevant capability map

| Capability | Evidence in this repository |
|---|---|
| Python AI application | FastAPI application and orchestration modules |
| AI Agent system | Planner, Router, Policy, Legal, Data, Verifier agents |
| AI Orchestration | Task planning → routing → parallel agent execution → verification |
| LangChain / LangGraph | Executable `StateGraph` runtime + `ChatOpenAI` specialist agents in `app/graph.py` |
| MCP | Official MCP Python SDK v2 server + in-process Client `tools/call` execution in `app/mcp/server.py` and `client.py` |
| RAG | Lightweight retriever in `app/rag/` |
| Multi-Agent | Specialized agent registry and orchestration |
| Deployment pipeline | Dockerfile, docker-compose, GitHub Actions CI |
| Operations | health endpoint, structured audit logging, retry/error handling |
| Governance | RBAC-style authorization, HITL gate, audit trail |

## Architecture

User request → Planner → Router → Specialized Agents → RAG / MCP Tools → Verifier → Risk/HITL → Response + Audit

## Quick start

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000` for the web UI or `/docs` for Swagger.

Example:

```bash
curl -X POST http://127.0.0.1:8000/orchestrate \
  -H "Content-Type: application/json" \
  -d '{"user":"analyst","question":"철도 역세권 개발 시 법령·정책·데이터 관점의 검토사항을 정리해줘"}'
```

## Docker

```bash
docker compose up --build
```

## Repository structure

```text
app/
  main.py              FastAPI entry point
  orchestrator.py      orchestration workflow
  registry.py          agent registry
  agents/              specialized agents
  rag/                 retrieval module
  mcp/                 MCP-style tool gateway and tools
  security/            authorization / HITL / audit
  graph.py             executable LangGraph workflow\n  mcp/server.py        official MCP v2 server\n  mcp/client.py        official MCP v2 client
.github/workflows/ci.yml
Dockerfile
docker-compose.yml
tests/
```

## Security / governance design

- Least-privilege tool authorization
- Human approval for high-risk actions
- Audit log for request, selected agents and outcome
- Tool allow-list
- No secrets committed to source control
- `.env` excluded through `.gitignore`

## Portfolio note

This is a **research prototype**, not a production government system. Replace sample RAG data and MCP-style tools with authorized data sources/APIs in a controlled environment before operational use.
