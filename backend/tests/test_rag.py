"""
Test RAG Vector Store & Ingestion Pipeline
"""

from backend.app.rag.ingest import parse_protocol_markdown, run_ingestion
from backend.app.rag.vectorstore import TriageVectorStore

def test_rag_ingest_and_query():
    store = run_ingestion()
    assert len(store.documents) > 0, "Ingested documents should not be empty"
    
    # Test query for anaphylaxis
    results = store.query("bee sting hives wheezing shortness of breath", top_k=2)
    assert len(results) > 0, "RAG query should return results"
    top_title = results[0].get("title", "")
    print(f"Top RAG Match: {top_title}")
    assert "ANAPHYLAXIS" in top_title.upper(), f"Expected Anaphylaxis protocol, got: {top_title}"
    print("✅ RAG pipeline test passed!")

if __name__ == "__main__":
    test_rag_ingest_and_query()
