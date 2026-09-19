def orchestration_score(result):
    plan=result.get("plan",[]); ctx=result.get("rag_context",[]); mcp=result.get("mcp_results",{})
    return {"agent_count":len(plan),"evidence_chunks":len(ctx),"official_results_present":bool(mcp.get("official_results")),"human_review":True}
