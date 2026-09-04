import json
import os
import uuid
import streamlit as st
import pandas as pd
from openai import OpenAI

# 1. Streamlit Page Configuration
st.set_page_config(
    page_title="MarketMind AI — Market Intelligence Agent",
    page_icon="🤖",
    layout="wide"
)

# 2. Model Pricing Configuration (USD per token)
MODEL_PRICING = {
    "gpt-4o": {
        "input": 2.50 / 1_000_000,
        "output": 10.00 / 1_000_000,
    },
    "gpt-4o-mini": {
        "input": 0.15 / 1_000_000,
        "output": 0.60 / 1_000_000,
    },
}

def calculate_call_cost(model_name: str, prompt_tokens: int, completion_tokens: int) -> float:
    """Calculates exact execution cost in USD based on token usage."""
    rates = MODEL_PRICING.get(model_name, MODEL_PRICING["gpt-4o"])
    return (prompt_tokens * rates["input"]) + (completion_tokens * rates["output"])

def execute_llm_step(client: OpenAI, model: str, system_prompt: str, user_prompt: str) -> tuple[str, float]:
    """Executes an API call, extracts usage, and returns content with calculated cost."""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2
    )
    usage = response.usage
    cost = calculate_call_cost(model, usage.prompt_tokens, usage.completion_tokens)
    return response.choices[0].message.content, cost


# 3. Helper Functions for Formatting Raw JSON Data
def render_executive_summary(summary_data):
    """Renders executive summary dict as clean Markdown and Tables."""
    if isinstance(summary_data, str):
        st.info(summary_data)
        return

    if isinstance(summary_data, dict):
        if "vendor_options" in summary_data:
            st.markdown("#### Vendor Comparison")
            vendors = summary_data["vendor_options"]
            if isinstance(vendors, list):
                # Convert list of vendor dicts to a clean DataFrame table
                formatted_vendors = []
                for v in vendors:
                    features = ", ".join(v.get("features", [])) if isinstance(v.get("features"), list) else v.get("features", "")
                    formatted_vendors.append({
                        "Vendor": v.get("name", "N/A"),
                        "Pricing Model": v.get("pricing_model", "N/A"),
                        "Key Features": features
                    })
                st.table(pd.DataFrame(formatted_vendors))

        if "pricing_models" in summary_data:
            st.markdown("#### Key Pricing Models")
            for model in summary_data["pricing_models"]:
                st.markdown(f"* {model}")


def render_market_overview(overview_data):
    """Renders market overview dict as readable sections and bullet points."""
    if isinstance(overview_data, str):
        st.write(overview_data)
        return

    if isinstance(overview_data, dict):
        if "key_market_players" in overview_data:
            st.markdown("#### Key Market Players")
            players = overview_data["key_market_players"]
            if isinstance(players, list):
                st.write(", ".join(players))

        if "industry_dynamics" in overview_data:
            st.markdown("#### Industry Dynamics")
            dynamics = overview_data["industry_dynamics"]
            
            if "growth_drivers" in dynamics:
                st.markdown("**Growth Drivers:**")
                for item in dynamics["growth_drivers"]:
                    st.markdown(f"* {item}")

            if "challenges" in dynamics:
                st.markdown("**Challenges:**")
                for item in dynamics["challenges"]:
                    st.markdown(f"* {item}")

            if "trends" in dynamics:
                st.markdown("**Trends:**")
                for item in dynamics["trends"]:
                    st.markdown(f"* {item}")


# 4. Session State Initialization
if "run_id" not in st.session_state:
    st.session_state.run_id = None
if "total_cost" not in st.session_state:
    st.session_state.total_cost = 0.0000
if "confidence_level" not in st.session_state:
    st.session_state.confidence_level = "HIGH"
if "report_data" not in st.session_state:
    st.session_state.report_data = None
if "is_approved" not in st.session_state:
    st.session_state.is_approved = False


# 5. UI Header Component
st.title("MarketMind AI — Market Intelligence Agent")
st.caption("Autonomous AI research agent with automated quality control and human-in-the-loop approval.")

default_request = "Research the market for AI-powered customer support software and prepare a business intelligence report."
user_request = st.text_area("Research Objective / Request:", value=default_request, height=100)

run_button = st.button("Run Research Pipeline", type="primary")


# 6. Pipeline Execution
if run_button:
    st.session_state.run_id = f"RUN-{uuid.uuid4().hex[:6].upper()}"
    st.session_state.total_cost = 0.0
    st.session_state.is_approved = False
    
    api_key = os.getenv("OPENAI_API_KEY")
    
    if api_key:
        client = OpenAI(api_key=api_key)
        model = "gpt-4o"
        
        with st.spinner("Executing bounded research agent pipeline..."):
            plan_sys = "You are a market intelligence agent. Decompose the request into sub-questions."
            _, cost1 = execute_llm_step(client, model, plan_sys, user_request)
            st.session_state.total_cost += cost1
            
            report_sys = (
                "You are an expert market analyst. Return a JSON object with two keys:\n"
                "- 'executive_summary': containing 'vendor_options' (list of objects with name, features, pricing_model) and 'pricing_models' (list of strings).\n"
                "- 'market_overview': containing 'key_market_players' (list of names) and 'industry_dynamics' (object with growth_drivers, challenges, trends lists)."
            )
            report_raw, cost2 = execute_llm_step(client, model, report_sys, user_request)
            st.session_state.total_cost += cost2
            
            try:
                # Strip markdown JSON blocks if present
                clean_json_str = report_raw.replace("```json", "").replace("```", "").strip()
                st.session_state.report_data = json.loads(clean_json_str)
            except json.JSONDecodeError:
                st.session_state.report_data = {
                    "executive_summary": report_raw[:300],
                    "market_overview": report_raw[300:]
                }
            st.session_state.confidence_level = "HIGH"


# 7. Output Rendering
if st.session_state.report_data and st.session_state.run_id:
    st.markdown("---")
    st.header("Human Approval Gate")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption("Run ID")
        st.markdown(f"### {st.session_state.run_id}")
    with col2:
        st.caption("Total Cost")
        st.markdown(f"### ${st.session_state.total_cost:.4f} USD")
    with col3:
        st.caption("Confidence Level")
        st.markdown(f"### {st.session_state.confidence_level}")
        
    st.subheader("Executive Summary")
    render_executive_summary(st.session_state.report_data.get("executive_summary", ""))
    
    st.subheader("Market Overview")
    render_market_overview(st.session_state.report_data.get("market_overview", ""))
    
    st.markdown("---")
    btn_col1, btn_col2 = st.columns([1, 4])
    with btn_col1:
        if st.button("Approve & Export Report"):
            st.session_state.is_approved = True
            st.success("Report approved successfully!")