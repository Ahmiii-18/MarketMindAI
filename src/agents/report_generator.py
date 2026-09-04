import json
from src.llm.client import LLMClient
from src.state.research_state import ResearchState
from src.schemas.report import ReportSchema

class ReportGenerator:
    def __init__(self, llm_client: LLMClient):
        self.client = llm_client

    def generate(self, state: ResearchState) -> ReportSchema:
        # Handle evidence whether it is a dict or a pydantic model
        evidence_summary = []
        for rec in state.evidence_store:
            if hasattr(rec, "model_dump"):
                evidence_summary.append(rec.model_dump())
            else:
                evidence_summary.append(rec)

        schema_json = json.dumps(ReportSchema.model_json_schema(), indent=2)

        system_prompt = (
            "You format synthesised research into a strict structured JSON report schema.\n\n"
            f"Your output MUST strictly follow this JSON Schema:\n{schema_json}"
        )

        prompt = f"""
        Assemble the final Market Intelligence Report using ONLY the provided evidence records.
        Objective: {state.plan.research_objective}
        Evidence Records: {json.dumps(evidence_summary)}
        Defects/Limitations: {json.dumps(state.defects)}

        Return only the raw JSON object matching the schema parameters directly.
        """

        response = self.client.chat_completion(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )

        raw_json = response.choices[0].message.content
        parsed = json.loads(raw_json)

        # Unpack if nested
        if "report" in parsed and isinstance(parsed["report"], dict):
            parsed = parsed["report"]

        return ReportSchema.model_validate(parsed)