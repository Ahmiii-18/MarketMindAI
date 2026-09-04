from typing import List, Optional
from pydantic import BaseModel
from src.schemas.evidence import EvidenceRecord

class Finding(BaseModel):
    statement: str
    claim_type: str
    evidence_ids: List[str]
    confidence: str

class ReportSchema(BaseModel):
    report_id: str
    research_objective: str
    executive_summary: str
    market_overview: str
    key_trends: List[Finding]
    competitor_matrix: List[dict]
    opportunities: List[Finding]
    risks: List[Finding]
    limitations_and_gaps: List[str]
    evidence_appendix: List[EvidenceRecord]
    confidence_level: str