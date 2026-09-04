from src.schemas.report import ReportSchema

class HumanApprovalGate:
    def prompt_reviewer(self, report: ReportSchema, cost_summary: dict) -> dict:
        print("\n" + "="*60)
        print(" HUMAN APPROVAL GATE - MARKETMIND AI REPORT REVIEW")
        print("="*60)
        print(f"Report ID : {report.report_id}")
        print(f"Objective : {report.research_objective}")
        print(f"Total Cost: ${cost_summary['total_cost_usd']} USD ({cost_summary['total_tokens']} tokens)")
        print(f"Confidence: {report.confidence_level}")
        print("-" * 60)
        print(f"Executive Summary Preview:\n{report.executive_summary[:200]}...\n")
        print("Select Action:")
        print("  [1] Approve & Publish")
        print("  [2] Reject Report")
        print("  [3] Request Additional Research")
        print("  [4] Modify Scope")

        choice = input("Enter choice (1-4): ").strip()
        
        actions = {
            "1": "approve",
            "2": "reject",
            "3": "request_research",
            "4": "modify_scope"
        }
        
        selected = actions.get(choice, "reject")
        reviewer_id = input("Enter Reviewer ID / Name: ").strip() if selected == "approve" else "N/A"
        
        return {
            "decision": selected,
            "approver_id": reviewer_id
        }