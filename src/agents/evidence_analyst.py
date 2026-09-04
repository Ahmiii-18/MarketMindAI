from src.schemas.evidence import EvidenceRecord

class EvidenceAnalyst:
    def __init__(self):
        self.record_counter = 0

    def process_tool_result(self, question_id: str, tool_name: str, result_data: dict) -> list[EvidenceRecord]:
        records = []
        if tool_name == "search_information" and isinstance(result_data, list):
            for item in result_data:
                self.record_counter += 1
                rec = EvidenceRecord(
                    evidence_id=f"EV-{self.record_counter:03d}",
                    question_id=question_id,
                    claim=item.get("snippet", ""),
                    claim_type="fact",
                    source_ref=item.get("id", "unknown"),
                    source_kind="search_result",
                    credibility="high",
                    confidence="high",
                    analyst_notes="Extracted directly from search corpus."
                )
                records.append(rec)
        return records