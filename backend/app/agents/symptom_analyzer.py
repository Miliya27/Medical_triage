"""
Agent 1: Symptom Analyzer Agent
Retrieves relevant medical protocols from local RAG (ChromaDB) and uses
the local Ollama LLM client to generate a structured medical assessment.
"""

from typing import Dict, Any, List, Optional
try:
    from backend.app.rag.vectorstore import TriageVectorStore
    from backend.app.rag.ingest import run_ingestion
    from backend.app.llm import OfflineLLMClient
except ImportError:
    from app.rag.vectorstore import TriageVectorStore
    from app.rag.ingest import run_ingestion
    from app.llm import OfflineLLMClient


class SymptomAnalyzerAgent:
    def __init__(self, vector_store: Optional[TriageVectorStore] = None, llm_client: Optional[OfflineLLMClient] = None):
        self.vector_store = vector_store or run_ingestion()
        self.llm_client = llm_client or OfflineLLMClient()

    def analyze(self, symptoms_text: str, patient_info: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Input: Free text patient symptoms (and optional patient demographic context)
        Output: Structured clinical assessment JSON with RAG citations
        """
        patient_info = patient_info or {}
        age = patient_info.get("age", "Unknown")
        gender = patient_info.get("gender", "Unknown")
        
        # 1. Retrieve relevant protocol chunks via RAG
        rag_results = self.vector_store.query(symptoms_text, top_k=3)
        context_str = "\n---\n".join([f"[{r['title']}]\n{r['text']}" for r in rag_results])
        
        # 2. Build structured LLM prompt
        system_prompt = (
            "You are an offline emergency medical triage assistant running on local edge hardware. "
            "Your task is to analyze patient symptoms using strictly provided medical protocol context "
            "and produce a structured clinical triage assessment in JSON format."
        )
        
        user_prompt = f"""PATIENT DEMOGRAPHICS:
Age: {age}, Gender: {gender}

PRESENTING SYMPTOMS & CHIEF COMPLAINT:
{symptoms_text}

RELEVANT WHO / FIRST-AID TRIAGE PROTOCOLS (RAG CONTEXT):
{context_str}

REQUIRED JSON OUTPUT FORMAT:
{{
  "suspected_conditions": ["Condition 1", "Condition 2"],
  "primary_concerns": ["Primary concern 1"],
  "urgency_level": "RED" | "YELLOW" | "GREEN",
  "triage_category": "Triage Category Name",
  "rationale": "Clinical rationale explaining decision based on RAG protocols",
  "recommended_actions": ["Immediate action 1", "Action 2"]
}}
"""

        # 3. Call local LLM client
        assessment = self.llm_client.generate_json(user_prompt, system_prompt=system_prompt)
        
        # Attach RAG citation metadata
        assessment["retrieved_protocols"] = [
            {"title": r.get("title"), "urgency": r.get("urgency"), "score": r.get("score")}
            for r in rag_results
        ]
        assessment["agent_id"] = "SymptomAnalyzerAgent"
        
        return assessment
