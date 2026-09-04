from typing import Dict, Any, List
from src.state.research_state import ResearchState

class QualityControlAgent:
    def evaluate(self, state: ResearchState) -> Dict[str, Any]:
        defects: List[str] = []
        
        if not state.evidence_store:
            defects.append("No evidence records were collected.")

        for i, record in enumerate(state.evidence_store):
            # Handle both dictionary and object attribute lookups safely
            if isinstance(record, dict):
                claim_type = record.get("claim_type")
                source_ref = record.get("source_ref")
            else:
                claim_type = getattr(record, "claim_type", None)
                source_ref = getattr(record, "source_ref", None)

            if claim_type == "fact" and not source_ref:
                defects.append(f"Evidence record {i} is marked as a fact but lacks a source_ref.")

        state.defects.extend(defects)

        return {
            "passed": len(defects) == 0,
            "defects": defects
        }