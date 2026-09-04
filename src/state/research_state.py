from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field
from src.schemas.plan import ResearchPlan

class ResearchState(BaseModel):
    run_id: str
    original_request: str
    plan: Optional[ResearchPlan] = None
    iteration_count: int = 0
    tool_call_count: int = 0
    is_completed: bool = False
    evidence_store: List[Dict[str, Any]] = Field(default_factory=list)
    defects: List[str] = Field(default_factory=list)
    tool_call_history: List[Dict[str, Any]] = Field(default_factory=list)

    def log_tool_call(self, tool_name: str, tool_args: Dict[str, Any], result: Any) -> None:
        """Logs details of an executed tool call and increments the counter."""
        self.tool_call_count += 1
        self.tool_call_history.append({
            "tool_name": tool_name,
            "tool_args": tool_args,
            "result": result
        })

    def add_evidence(self, evidence: Any) -> None:
        """Appends a new evidence record to the evidence store."""
        if hasattr(evidence, "model_dump"):
            self.evidence_store.append(evidence.model_dump())
        elif isinstance(evidence, dict):
            self.evidence_store.append(evidence)
        else:
            self.evidence_store.append({"content": str(evidence)})