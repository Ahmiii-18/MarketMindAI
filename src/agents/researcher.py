import json
from src.llm.client import LLMClient
from src.tools.registry import TOOL_SCHEMAS
from src.tools.dispatcher import ToolDispatcher
from src.state.research_state import ResearchState
from src.agents.evidence_analyst import EvidenceAnalyst
from src.config import config

class ResearchAgentLoop:
    def __init__(self, llm_client: LLMClient, dispatcher: ToolDispatcher):
        self.client = llm_client
        self.dispatcher = dispatcher
        self.analyst = EvidenceAnalyst()

    def run(self, state: ResearchState):
        system_prompt = (
            "You are an Autonomous Business Research Agent. Call available tools to collect evidence "
            "answering the plan's sub-questions. Signal completion when sufficient evidence is gathered."
        )

        while state.iteration_count < config.max_iterations and state.tool_call_count < config.max_tool_calls:
            state.iteration_count += 1
            
            # Select target open question
            open_question = state.plan.objectives[0].sub_questions[0]
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Gather evidence for sub-question [{open_question.id}]: {open_question.question_text}"}
            ]

            response = self.client.chat_completion(
                messages=messages,
                tools=TOOL_SCHEMAS
            )

            msg = response.choices[0].message
            if msg.tool_calls:
                for tool_call in msg.tool_calls:
                    t_name = tool_call.function.name
                    t_args = tool_call.function.arguments
                    
                    # Dispatch tool call safely
                    res = self.dispatcher.dispatch(t_name, t_args)
                    state.log_tool_call(t_name, t_args, res)
                    
                    # Process evidence
                    if res.get("status") == "success":
                        records = self.analyst.process_tool_result(open_question.id, t_name, res.get("data"))
                        for rec in records:
                            state.add_evidence(rec)
            else:
                # Agent indicates finished researching
                break

        state.is_completed = True