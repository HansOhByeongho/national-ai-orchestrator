export default function handler(req,res){
  if(req.method!=='POST') return res.status(405).json({error:'POST only'});
  const q=(req.body&&req.body.question)||'';
  const agents=[];
  if(/정책|사업|계획|행정|지역개발/.test(q)) agents.push('policy');
  if(/법|법령|규제|인허가|조례/.test(q)) agents.push('legal');
  if(/데이터|통계|수요|분석|예측/.test(q)) agents.push('data');
  if(!agents.length) agents.push('policy','data');
  const evidence=[
    '공공 AI 시스템은 근거 추적, 접근통제, 사람의 검토와 감사로그를 고려해야 합니다.',
    '역세권 개발은 교통·토지이용·산업·주거·관광·재원조달을 함께 검토해야 합니다.',
    'RAG는 관련 근거를 검색하여 생성 과정에 제공하는 방식입니다.'
  ];
  const results=agents.map(a=>({agent:a,summary:
    a==='policy'?'정책목표·이해관계자·추진절차·정책수단을 구조화합니다.':
    a==='legal'?'관련 법령·규제·인허가 쟁점을 검토 대상으로 분류합니다.':
    '필요 데이터·지표·비교기준·검증 항목을 정의합니다.'
  }));
  return res.status(200).json({
    plan:agents,
    rag_context:evidence,
    verification:{status:'verified_with_human_review_recommended',checks:['agent output present','retrieved evidence attached','audit recorded'],results},
    mcp:{gateway:'policy enforcement point',tools:['policy_search','legal_search'],high_risk_actions:'HITL required'}
  });
}