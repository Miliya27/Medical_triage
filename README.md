# Offline Multi-Agent Medical Triage System 🏥⚡

An open-source, 100% offline-first medical triage assistant built for disaster response zones, remote off-grid clinics, and zero-connectivity field environments.

## 🚀 Key Features

- **100% Offline Capability**: Runs completely on local hardware. No cloud APIs, no remote database calls, no CDN dependencies.
- **3-Agent Pipeline**:
  1. **Symptom Analyzer Agent**: RAG engine over WHO & standard first-aid protocols using local ChromaDB + Ollama LLM (`llama3.2:3b` / `phi3:mini`) for structured assessment.
  2. **Drug/Interaction Checker Agent**: Cross-references patient medications and allergies against a bundled local open formulary database.
  3. **Escalation Agent**: Combines symptom analysis, drug contraindications, and real/simulated patient vitals to generate a triaged severity tier (Red/Yellow/Green) and responder alert status.
- **Vitals Integration**: Real-time BLE sensor reader (`bleak`) with built-in realistic vitals simulator for testing.
- **Local Persistence**: SQLite database storing patient records, triage logs, and agent decision histories.
- **Modern UI**: High-performance React + Vite + Tailwind CSS dashboard bundled locally.

---

## 🏗️ System Architecture

```
+-------------------------------------------------------------------------+
|                              React Frontend                             |
|       (Triage Input, Step-by-Step Agent Execution, Vitals Monitor)      |
+-------------------------------------------------------------------------+
                                     │
                                     ▼ (Local HTTP / REST)
+-------------------------------------------------------------------------+
|                             FastAPI Backend                             |
|                                                                         |
|  +---------------------+  +---------------------+  +------------------+ |
|  |  Agent 1: Symptom   |  |   Agent 2: Drug     |  | Agent 3:         | |
|  |  Analyzer (RAG+LLM) |─►|   Interaction       |─►| Escalation &     | |
|  +---------------------+  +---------------------+  | Severity Tier    | |
|             │                        │             +------------------+ |
|             ▼                        ▼                      ▲           |
|    Local ChromaDB Vector    Local Formulary DB              │           |
|    (WHO Protocols RAG)     (JSON Contraindications)         │           |
|             │                                               │           |
|             ▼                                               │           |
|      Local Ollama LLM                                 Local Vitals      |
|    (llama3.2:3b/phi3:mini)                        (BLE / Simulated)  |
+-------------------------------------------------------------------------+
                                     │
                                     ▼
+-------------------------------------------------------------------------+
|                           SQLite Local Storage                          |
|             (Patient Encounters, Triage Logs, Audit Trails)             |
+-------------------------------------------------------------------------+
```

---

## 🛠️ Quick Setup (Offline Mode Ready)

### Prerequisites
1. **Python 3.11+**
2. **Node.js 18+**
3. **Ollama** installed locally (`ollama pull llama3.2:3b` or `ollama pull phi3:mini`)

### Backend Setup
```bash
cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
python app/rag/ingest.py # Build local vector store
python -m uvicorn app.main:app --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

---

## 📜 License
[MIT License](LICENSE)
