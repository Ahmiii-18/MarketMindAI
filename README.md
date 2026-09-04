# MarketMind AI — Market Intelligence Agent

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://marketmindaii.streamlit.app/)

MarketMind AI is an autonomous business research agent designed to generate management consultancy market intelligence briefs. Built directly in native Python, it features schema-validated tool calling, epistemic evidence tracking, real-time API cost calculation, and a Human Approval Gate prior to final report export.

🚀 **Live Demo**: [marketmindaii.streamlit.app](https://marketmindaii.streamlit.app/)

---

## Key Features

* **Native Orchestration**: Bounded agent state machine, tool dispatcher, and execution loop implemented in native Python without relying on prebuilt agent wrappers.
* **Token-Accurate Cost Tracking**: Tracks exact token usage per API call and aggregates cumulative execution costs in USD.
* **Structured UI Rendering**: Validates JSON contracts and automatically formats output into clean tables, comparative summaries, and market breakdowns.
* **Human Approval Gate**: Provides a review panel displaying Run ID, total cost, confidence metrics, and findings before report finalization.
* **Epistemic Classification**: Categorizes research evidence into *Fact*, *Inference*, *Recommendation*, and *Uncertainty*.

---

## System Architecture

1. **Intake & Planning**: Decomposes broad research requests into 3–6 answerable sub-questions.
2. **Bounded Execution Loop**: Dispatches schema-validated tool calls with strict permission controls and iteration caps.
3. **Evidence Store**: Records research facts and metadata tied directly to tool source references.
4. **Quality Control & Human Gate**: Evaluates coverage, triggers repair cycles if necessary, and holds output for human sign-off.

---

## Installation & Setup

### Prerequisites

* Python 3.10+
* OpenAI API Key

### Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone [https://github.com/](https://github.com/)<Ahmiii-18>/MarketMind-AI.git
   cd MarketMind-AI
