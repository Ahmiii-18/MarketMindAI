import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class Config(BaseModel):
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    default_model: str = os.getenv("DEFAULT_MODEL", "gpt-4o")
    reasoning_model: str = os.getenv("REASONING_MODEL", "gpt-4o")
    max_iterations: int = int(os.getenv("MAX_ITERATIONS", "10"))
    max_tool_calls: int = int(os.getenv("MAX_TOOL_CALLS", "15"))
    run_budget_usd: float = float(os.getenv("RUN_BUDGET_USD", "2.00"))

    def validate_keys(self):
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY is missing from environment variables.")

config = Config()