from .base import BaseAgent, AgentResult

class PolicyAgent(BaseAgent):
    name = "policy"; keywords = ("정책", "사업", "계획", "행정", "지역개발")
    def run(self, question, context): return AgentResult(self.name, "정책목표, 이해관계자, 추진절차와 정책수단을 구조화했습니다.", context[:2])

class LegalAgent(BaseAgent):
    name = "legal"; keywords = ("법", "법령", "규제", "인허가", "조례")
    def run(self, question, context): return AgentResult(self.name, "관련 법령·규제·인허가 쟁점을 검토 대상으로 분류했습니다.", context[:2])

class DataAgent(BaseAgent):
    name = "data"; keywords = ("데이터", "통계", "수요", "분석", "예측")
    def run(self, question, context): return AgentResult(self.name, "필요 데이터, 지표, 비교기준과 검증 항목을 정의했습니다.", context[:2])
