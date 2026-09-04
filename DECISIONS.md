# Architecture & Design Decisions (DECISIONS.md)

This document records the architectural, algorithmic, and tooling choices for the Offline Multi-Agent Medical Triage System.

---

## 1. Local LLM Selection: Ollama with `llama3.2:3b` vs `phi3:mini`

### Decision
Primary model target: **`llama3.2:3b`** (with fallback option to **`phi3:mini`**).

### Rationale
- **Inference Speed & Memory Footprint**: Both `llama3.2:3b` (Q4_K_M quant ~2.0GB RAM) and `phi3:mini` (~2.3GB RAM) run smoothly on low-power laptop CPU/GPU hardware without internet connectivity.
- **Instruction Following for JSON Outputs**: `llama3.2:3b` demonstrates superior structured JSON extraction capabilities required for Agent 1 (Symptom Assessment schema) and Agent 3 (Triage Tier schema).
- **Latency Benchmark Target**: < 3.5s per agent pipeline step on consumer hardware.

---

## 2. Embedding Model: `sentence-transformers/all-MiniLM-L6-v2`

### Decision
Use `all-MiniLM-L6-v2` cached locally in the backend directory.

### Rationale
- **Size & Performance**: At ~90MB, `all-MiniLM-L6-v2` offers standard medical text retrieval accuracy with minimal memory usage.
- **Offline Guarantee**: The model files are loaded directly from disk without touching HuggingFace hub at runtime.

---

## 3. Vector Database: ChromaDB (Local Persistent Storage)

### Decision
Use `chromadb` with `PersistentClient(path="./chroma_db")`.

### Rationale
- Pure Python/C++ local storage without needing a Docker container, external service, or cloud server.
- Supports vector query operations with < 20ms response time.

---

## 4. Multi-Agent Pipeline Architecture

### Decision
Partition triage processing into 3 modular single-responsibility agents rather than 1 monolithic prompt:
1. **Symptom Analyzer Agent**: Focuses strictly on symptom extraction, RAG protocol retrieval, and differential assessment.
2. **Drug/Interaction Checker Agent**: Deterministic cross-checking of medications/allergies against static local formulary dataset (OpenFDA JSON export format).
3. **Escalation Agent**: Rule-based + LLM synthesis combining Agent 1 & Agent 2 outputs with patient vitals to determine urgency (Red / Yellow / Green tier).

### Rationale
- **Safety & Legibility**: Medical safety requires deterministic drug interaction rules, which shouldn't rely solely on LLM generation. Separating Agent 2 guarantees zero LLM hallucinations for drug contraindications.

---

## 5. Hardware Vitals Integration & Simulation

### Decision
Implement a dual-mode vitals engine:
- **BLE Reader**: Uses `bleak` Python library to scan and stream real pulse oximeter / heart rate monitor data over Bluetooth Low Energy.
- **Simulated Engine**: Generates realistic synthetic vitals (Heart Rate, SpO2, Systolic/Diastolic BP, Respiration Rate, Temperature) with interactive preset scenarios (e.g. Anaphylaxis, Sepsis, Stable).

### Rationale
Guarantees full demo reliability during hackathons and testing even when physical BLE hardware is unavailable.
