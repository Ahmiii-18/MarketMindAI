# Simulated Local Corpus for reproducible execution
CORPUS = {
    "doc_1": "Vendor Alpha offers AI customer support software with entry pricing starting at $49/seat/month. It includes basic NLP routing.",
    "doc_2": "Vendor Beta provides enterprise support AI at $99/seat/month, focusing heavily on custom workflow automations.",
    "doc_3": "Vendor Gamma customer support platform pricing is undisclosed; custom quotes require contacting sales."
}

def search_information(query: str, max_results: int = 5) -> list:
    results = []
    for doc_id, text in CORPUS.items():
        if any(term.lower() in text.lower() for term in query.split()):
            results.append({"id": doc_id, "snippet": text})
    return results[:max_results]

def retrieve_document(document_id: str) -> dict:
    if document_id in CORPUS:
        return {"id": document_id, "content": CORPUS[document_id]}
    return {"error": f"Document ID '{document_id}' not found in index."}

def calculate_metric(operation: str, values: list) -> dict:
    if operation == "average" and values:
        res = sum(values) / len(values)
        return {"operation": operation, "result": res, "inputs": values}
    return {"error": "Unsupported operation or empty values."}

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "search_information",
            "description": "Searches the local corpus for information relevant to the query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "max_results": {"type": "integer", "default": 5}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "retrieve_document",
            "description": "Retrieves the full text of a specific document by ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "document_id": {"type": "string"}
                },
                "required": ["document_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_metric",
            "description": "Performs deterministic calculations on numerical values.",
            "parameters": {
                "type": "object",
                "properties": {
                    "operation": {"type": "string", "enum": ["average", "growth_rate"]},
                    "values": {"type": "array", "items": {"type": "number"}}
                },
                "required": ["operation", "values"]
            }
        }
    }
]