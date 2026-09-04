import json
from src.llm.client import LLMClient
from src.schemas.plan import ResearchPlan

class ResearchPlanner:
    def __init__(self, llm_client: LLMClient):
        self.client = llm_client

    def generate_plan(self, user_request: str) -> ResearchPlan:
        schema_json = json.dumps(ResearchPlan.model_json_schema(), indent=2)
        
        system_prompt = (
            "You are a Senior Strategic Research Planner. Decompose the client's request into a "
            "structured research plan with answerable sub-questions.\n\n"
            f"Your output MUST strictly follow this JSON Schema:\n{schema_json}"
        )
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Request: {user_request}\nOutput pure JSON matching the schema directly."}
        ]
        
        response = self.client.chat_completion(
            messages=messages,
            response_format={"type": "json_object"}
        )
        
        raw_json = response.choices[0].message.content
        parsed = json.loads(raw_json)
        
        if "research_plan" in parsed and isinstance(parsed["research_plan"], dict):
            parsed = parsed["research_plan"]

        return ResearchPlan.model_validate(parsed)