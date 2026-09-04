class UsageTracker:
    def __init__(self):
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.total_cost = 0.0

    def record_usage(self, prompt_tokens: int, completion_tokens: int, model: str = "gpt-4o"):
        self.total_prompt_tokens += prompt_tokens
        self.total_completion_tokens += completion_tokens
        # Estimated cost mapping for gpt-4o ($2.50 / 1M prompt, $10.00 / 1M completion)
        cost = (prompt_tokens * 2.50 / 1_000_000) + (completion_tokens * 10.00 / 1_000_000)
        self.total_cost += cost

    def get_summary(self):
        return {
            "prompt_tokens": self.total_prompt_tokens,
            "completion_tokens": self.total_completion_tokens,
            "total_tokens": self.total_prompt_tokens + self.total_completion_tokens,
            "total_cost_usd": round(self.total_cost, 4)
        }