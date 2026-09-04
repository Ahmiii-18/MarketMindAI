import uuid
import json
from src.llm.usage import UsageTracker
from src.llm.client import LLMClient
from src.tools.dispatcher import ToolDispatcher
from src.state.research_state import ResearchState
from src.agents.planner import ResearchPlanner
from src.agents.researcher import ResearchAgentLoop
from src.agents.quality_control import QualityControlAgent
from src.agents.report_generator import ReportGenerator
from src.approval.cli_gate import HumanApprovalGate

def run_marketmind_pipeline(user_prompt: str):
    run_id = f"RUN-{uuid.uuid4().hex[:6].upper()}"
    usage_tracker = UsageTracker()
    llm_client = LLMClient(usage_tracker)
    dispatcher = ToolDispatcher()

    print(f"[*] Initializing MarketMind AI Pipeline (Run ID: {run_id})...")

    # 1. State Initialization
    state = ResearchState(run_id=run_id, original_request=user_prompt)

    # 2. Research Planning
    print("[*] Stage 1: Decomposing request into Research Plan...")
    planner = ResearchPlanner(llm_client)
    state.plan = planner.generate_plan(user_prompt)
    print(f"    -> Generated Plan with {len(state.plan.objectives)} strategic objectives.")

    # 3. Multi-step Agent Loop
    print("[*] Stage 2: Executing Bounded Agent Research Loop...")
    research_loop = ResearchAgentLoop(llm_client, dispatcher)
    research_loop.run(state)
    print(f"    -> Research completed in {state.iteration_count} iterations ({state.tool_call_count} tool calls).")
    print(f"    -> Evidence Store holds {len(state.evidence_store)} records.")

    # 4. Quality Control Evaluation
    print("[*] Stage 3: Running Automated Quality Control Pass...")
    qc = QualityControlAgent()
    qc_result = qc.evaluate(state)
    print(f"    -> QC Status: {'PASS' if qc_result['passed'] else 'FAIL'}")
    if not qc_result['passed']:
        print(f"    -> Detected Defects: {qc_result['defects']}")

    # 5. Report Generation
    print("[*] Stage 4: Synthesizing Final Market Intelligence Report...")
    generator = ReportGenerator(llm_client)
    report = generator.generate(state)

    # 6. Human Approval Gate
    gate = HumanApprovalGate()
    decision = gate.prompt_reviewer(report, usage_tracker.get_summary())

    # 7. Final Action
    if decision["decision"] == "approve":
        print(f"\n[+] Report Approved by {decision['approver_id']}. Saving final published artefact...")
        with open(f"report_{run_id}.json", "w") as f:
            f.write(report.model_dump_json(indent=2))
        print(f"[+] Final Report published to report_{run_id}.json")
    else:
        print(f"\n[-] Report action resolved to '{decision['decision']}'. Publication aborted.")

if __name__ == "__main__":
    sample_request = "Research the market for AI-powered customer support software and prepare a business intelligence report."
    run_marketmind_pipeline(sample_request)