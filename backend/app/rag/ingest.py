"""
Knowledge Base Ingestion Script
Parses Markdown protocol files into structured chunks and populates the local vector store.
"""

import os
import re
from typing import List, Dict, Any
try:
    from backend.app.rag.vectorstore import TriageVectorStore
except ImportError:
    from app.rag.vectorstore import TriageVectorStore


PROTOCOLS_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "data", "knowledge_base", "triage_protocols.md"
)

def parse_protocol_markdown(filepath: str) -> List[Dict[str, Any]]:
    if not os.path.exists(filepath):
        print(f"❌ Protocol file not found at {filepath}")
        return []

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Split by section headers starting with '## PROTOCOL'
    sections = re.split(r'\n(?=## PROTOCOL)', content)
    chunks = []

    for idx, sec in enumerate(sections):
        sec = sec.strip()
        if not sec:
            continue

        lines = sec.split("\n")
        title_line = lines[0].replace("#", "").strip()
        
        # Determine urgency tag from text if present
        urgency = "UNKNOWN"
        if "RED" in sec:
            urgency = "RED"
        elif "YELLOW" in sec:
            urgency = "YELLOW"
        elif "GREEN" in sec:
            urgency = "GREEN"

        chunks.append({
            "id": f"protocol_{idx + 1}",
            "title": title_line,
            "text": sec,
            "urgency": urgency
        })

    return chunks

def run_ingestion() -> TriageVectorStore:
    print("📖 Parsing WHO & START Triage Protocol Knowledge Base...")
    chunks = parse_protocol_markdown(PROTOCOLS_FILE)
    print(f"🧩 Parsed {len(chunks)} protocol chunks.")

    store = TriageVectorStore()
    store.add_documents(chunks)
    print("✅ RAG Knowledge Base Ingestion complete.")
    return store

if __name__ == "__main__":
    run_ingestion()
