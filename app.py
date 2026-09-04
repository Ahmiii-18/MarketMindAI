import uuid
import json
import pandas as pd
import streamlit as st

from src.llm.usage import UsageTracker
from src.llm.client import LLMClient
from src.tools.dispatcher import ToolDispatcher
from src.state.research_state import ResearchState
from src.agents.planner import ResearchPlanner
from src.agents.researcher import ResearchAgentLoop
from src.agents.quality_control import QualityControlAgent
from src.agents.report_generator import ReportGenerator

st.set_page_config(page_title="MarketMind AI", layout="wide")

st.title("MarketMind AI — Market Intelligence Agent")
st.caption("Autonomous AI research agent with automated quality control and human-in-the-loop approval.")

# Session state initialization
if "report" not in st.session_state:
    st.session_state.report = None
if "run_id" not in st.session_state:
    st.session_state.run_id = None
if "usage" not in st.session_state:
    st.session_state.usage = None
if "approval_status" not in st.session_state:
    st.session_state.approval_status = None

user_prompt = st.text_area(
    "Research Objective / Request:",
    value="Research the market for AI-powered customer support software and prepare a business intelligence report.",
    height=80
)

if st.button("Run Research Pipeline", type="primary"):
    st.session_state.report = None
    st.session_state.approval_status = None
    
    with st.status("Executing MarketMind Research Pipeline...", expanded=True) as status:
        run_id = f"RUN-{uuid.uuid4().hex[:6].upper()}"
        usage_tracker = UsageTracker()
        llm_client = LLMClient(usage_tracker)
        dispatcher = ToolDispatcher()

        # 1. State Initialization
        st.write("Step 1: Initializing Research State...")
        state = ResearchState(run_id=run_id, original_request=user_prompt)

        # 2. Research Planning
        st.write("Step 2: Planning strategic objectives...")
        planner = ResearchPlanner(llm_client)
        state.plan = planner.generate_plan(user_prompt)
        st.write(f"-> Generated Plan with {len(state.plan.objectives)} strategic objectives.")

        # 3. Multi-step Agent Loop
        st.write("Step 3: Gathering evidence via autonomous loop...")
        research_loop = ResearchAgentLoop(llm_client, dispatcher)
        research_loop.run(state)
        st.write(f"-> Executed {state.iteration_count} iterations and collected {len(state.evidence_store)} evidence items.")

        # 4. Quality Control
        st.write("Step 4: Performing Quality Control checks...")
        qc = QualityControlAgent()
        qc_result = qc.evaluate(state)
        st.write(f"-> QC Status: {'PASS' if qc_result['passed'] else 'FAIL'}")

        # 5. Report Generation
        st.write("Step 5: Synthesizing final JSON report...")
        generator = ReportGenerator(llm_client)
        report = generator.generate(state)

        # Save results to Streamlit state
        st.session_state.report = report
        st.session_state.run_id = run_id
        st.session_state.usage = usage_tracker.get_summary()
        status.update(label="Pipeline Completed Successfully!", state="complete", expanded=False)

# Human Approval Gate UI
if st.session_state.report:
    st.divider()
    st.header("Human Approval Gate")
    
    report_dict = st.session_state.report.model_dump()
    
    # Overview Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Run ID", st.session_state.run_id)
    with col2:
        cost = st.session_state.usage.get("total_cost", 0.0) if st.session_state.usage else 0.0
        st.metric("Total Cost", f"${cost:.4f} USD")
    with col3:
        st.metric("Confidence Level", report_dict.get("confidence_level", "high").upper())

    # Executive Summary & Market Overview
    st.subheader("Executive Summary")
    st.info(report_dict.get("executive_summary", ""))

    st.subheader("Market Overview")
    st.write(report_dict.get("market_overview", ""))

    # Tabbed Interface for Visual Reports
    tab1, tab2, tab3, tab4 = st.tabs(["Competitor Matrix", "Key Trends", "Opportunities & Risks", "Raw JSON"])
    
    with tab1:
        matrix = report_dict.get("competitor_matrix", [])
        if matrix:
            st.dataframe(pd.DataFrame(matrix), use_container_width=True)
        else:
            st.write("No competitor matrix data available.")
            
    with tab2:
        trends = report_dict.get("key_trends", [])
        for t in trends:
            st.markdown(f"- **{t.get('statement')}** *(Type: {t.get('claim_type')}, Confidence: {t.get('confidence')})*")

    with tab3:
        col_opp, col_risk = st.columns(2)
        with col_opp:
            st.markdown("#### Opportunities")
            for opp in report_dict.get("opportunities", []):
                st.success(opp.get("statement"))
        with col_risk:
            st.markdown("#### Risks")
            for r in report_dict.get("risks", []):
                st.warning(r.get("statement"))

    with tab4:
        st.json(report_dict)

    st.divider()
    
    # Approval Action Section
    st.subheader("Sign-off & Publication Decision")
    approver = st.text_input("Reviewer Name / ID:", value="Ahmad")

    btn_col1, btn_col2, _ = st.columns([1, 1, 2])
    
    with btn_col1:
        if st.button("Approve & Publish", type="primary"):
            filename = f"report_{st.session_state.run_id}.json"
            with open(filename, "w") as f:
                f.write(st.session_state.report.model_dump_json(indent=2))
            st.session_state.approval_status = f"Approved by {approver}. Report published to `{filename}`"

    with btn_col2:
        if st.button("Reject Report"):
            st.session_state.approval_status = "Rejected"

    if st.session_state.approval_status:
        if "Approved" in st.session_state.approval_status:
            st.success(f"[+] {st.session_state.approval_status}")
        else:
            st.error("[-] Report action resolved to Rejected. Publication aborted.")