from typing import List, Literal, Optional
from pydantic import BaseModel

class EvidenceRecord(BaseModel):
    evidence_id: str
    question_id: str
    claim: str
    claim_type: Literal["fact", "inference", "recommendation", "uncertainty"]
    source_ref: str
    source_kind: Literal["retrieved_document", "search_result", "calculation", "model_generated"]
    credibility: Literal["high", "medium", "low", "unknown"]
    confidence: Literal["high", "medium", "low"]
    analyst_notes: Optional[str] = ""