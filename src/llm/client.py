from openai import OpenAI
from src.config import config
from src.llm.usage import UsageTracker

class LLMClient:
    def __init__(self, usage_tracker: UsageTracker):
        config.validate_keys()
        self.client = OpenAI(api_key=config.openai_api_key)
        self.tracker = usage_tracker

    def chat_completion(self, messages, model=None, temperature=0.2, tools=None, response_format=None):
        selected_model = model or config.default_model
        kwargs = {
            "model": selected_model,
            "messages": messages,
            "temperature": temperature,
        }
        if tools:
            kwargs["tools"] = tools
        if response_format:
            kwargs["response_format"] = response_format

        response = self.client.chat.completions.create(**kwargs)
        
        if response.usage:
            self.tracker.record_usage(
                response.usage.prompt_tokens,
                response.usage.completion_tokens,
                selected_model
            )
            
        return response