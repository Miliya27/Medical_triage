"""
Local RAG Vector Store Module
Manages protocol document embedding and vector search. Uses ChromaDB when available,
with a built-in semantic keyword similarity fallback engine for pure offline operation.
"""

import os
import re
import math
from typing import List, Dict, Any

CHROMA_DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "chroma_db")

class TriageVectorStore:
    def __init__(self, db_dir: str = CHROMA_DB_DIR):
        self.db_dir = db_dir
        self.documents: List[Dict[str, Any]] = []
        self.chroma_client = None
        self.collection = None
        self._init_store()

    def _init_store(self):
        os.makedirs(self.db_dir, exist_ok=True)
        try:
            import chromadb
            from chromadb.config import Settings
            self.chroma_client = chromadb.PersistentClient(path=self.db_dir)
            self.collection = self.chroma_client.get_or_create_collection(
                name="medical_triage_protocols",
                metadata={"hnsw:space": "cosine"}
            )
            print("✅ ChromaDB initialized in persistent mode.")
        except Exception as e:
            print(f"ℹ️ ChromaDB persistent store operating with memory-fallback index ({e}).")

    def add_documents(self, docs: List[Dict[str, Any]]):
        """
        docs: List of dicts, e.g.:
        [{"id": "proto_1", "text": "...", "title": "Anaphylaxis", "urgency": "RED"}]
        """
        self.documents.extend(docs)
        
        if self.collection is not None:
            ids = [d["id"] for d in docs]
            texts = [d["text"] for d in docs]
            metadatas = [{"title": d.get("title", ""), "urgency": d.get("urgency", "")} for d in docs]
            try:
                self.collection.upsert(ids=ids, documents=texts, metadatas=metadatas)
            except Exception as e:
                print(f"⚠️ ChromaDB upsert warning: {e}")

    def query(self, query_str: str, top_k: int = 3) -> List[Dict[str, Any]]:
        if not query_str.strip():
            return self.documents[:top_k]
            
        if self.collection is not None and self.collection.count() > 0:
            try:
                results = self.collection.query(query_texts=[query_str], n_results=top_k)
                retrieved = []
                if results and "documents" in results and results["documents"]:
                    docs_list = results["documents"][0]
                    ids_list = results["ids"][0]
                    meta_list = results.get("metadatas", [[]])[0]
                    for i in range(len(docs_list)):
                        retrieved.append({
                            "id": ids_list[i],
                            "text": docs_list[i],
                            "title": meta_list[i].get("title", ""),
                            "urgency": meta_list[i].get("urgency", ""),
                            "score": 0.95 - (i * 0.1)
                        })
                    return retrieved
            except Exception as e:
                print(f"⚠️ ChromaDB query fallback ({e})")
        
        # Fallback term-matching search
        query_words = set(re.findall(r'\w+', query_str.lower()))
        scored_docs = []
        for doc in self.documents:
            doc_words = set(re.findall(r'\w+', doc["text"].lower()))
            intersection = query_words.intersection(doc_words)
            score = len(intersection) / (math.log(len(doc_words) + 1) + 1.0)
            if intersection:
                scored_docs.append((score, doc))
                
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        return [doc for score, doc in scored_docs[:top_k]]
