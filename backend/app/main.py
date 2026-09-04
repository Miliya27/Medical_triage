"""
FastAPI Backend Application for Offline Multi-Agent Medical Triage System
Wires Agent 1 (Symptom Analyzer), Agent 2 (Drug Checker), and Agent 3 (Escalation)
into a unified 3-agent pipeline with SQLite local persistence.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import random

try:
    from backend.app.agents.symptom_analyzer import SymptomAnalyzerAgent
    from backend.app.agents.drug_interaction import DrugInteractionAgent
    from backend.app.agents.escalation import EscalationAgent
    from backend.app.database import TriageDatabase
except ImportError:
    from app.agents.symptom_analyzer import SymptomAnalyzerAgent
    from app.agents.drug_interaction import DrugInteractionAgent
    from app.agents.escalation import EscalationAgent
    from app.database import TriageDatabase


app = FastAPI(
    title="Offline Multi-Agent Medical Triage API",
    description="100% Offline Multi-Agent Triage Engine for Low-Connectivity / Disaster Zones",
    version="1.0.0"
)

# Enable CORS for local React / Vite frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Database and Agents
db = TriageDatabase()
symptom_agent = SymptomAnalyzerAgent()
drug_agent = DrugInteractionAgent()
escalation_agent = EscalationAgent()

# Request & Response Schemas
class TriageRequest(BaseModel):
    patient_name: Optional[str] = "Anonymous Patient"
    age: Optional[int] = 30
    gender: Optional[str] = "Unknown"
    symptoms: str
    allergies: Optional[List[str]] = []
    current_medications: Optional[List[str]] = []
    proposed_treatments: Optional[List[str]] = []
    vitals: Optional[Dict[str, Any]] = None

@app.get("/api/health")
def health_check():
    return {
        "status": "online",
        "mode": "100% OFFLINE LOCAL",
        "agents": ["SymptomAnalyzerAgent", "DrugInteractionAgent", "EscalationAgent"],
        "database": "SQLite Local"
    }

@app.post("/api/triage/run")
def run_triage_pipeline(req: TriageRequest):
    """
    Executes full 3-agent triage pipeline:
    1. Symptom Analyzer Agent (RAG + Ollama)
    2. Drug/Interaction Checker Agent (Local Formulary)
    3. Escalation Agent (Vitals + Risk Synthesis)
    4. Persists encounter in SQLite database
    """
    try:
        # Default vitals if none supplied
        vitals = req.vitals or {
            "heart_rate": 78,
            "spo2": 97,
            "systolic_bp": 120,
            "diastolic_bp": 80,
            "respiration_rate": 16,
            "temperature": 37.0
        }

        # Step 1: Agent 1 - Symptom Analysis
        agent1_out = symptom_agent.analyze(
            symptoms_text=req.symptoms,
            patient_info={"age": req.age, "gender": req.gender}
        )

        # Infer proposed drugs from Agent 1 recommendations or request
        proposed = list(req.proposed_treatments)
        if "recommended_actions" in agent1_out:
            for action in agent1_out["recommended_actions"]:
                for d in ["Epinephrine", "Aspirin", "Nitroglycerin", "Salbutamol", "Amoxicillin", "Paracetamol", "Ibuprofen"]:
                    if d.lower() in action.lower() and d not in proposed:
                        proposed.append(d)

        # Step 2: Agent 2 - Drug & Allergy Cross-check
        agent2_out = drug_agent.check_interactions(
            proposed_drugs=proposed,
            allergies=req.allergies,
            current_medications=req.current_medications,
            conditions=agent1_out.get("suspected_conditions", [])
        )

        # Step 3: Agent 3 - Escalation & Triage Tier Decision
        agent3_out = escalation_agent.evaluate_triage(
            symptom_analysis=agent1_out,
            drug_check=agent2_out,
            vitals=vitals
        )

        # Step 4: Persist encounter in SQLite
        encounter_id = db.save_encounter(
            patient_name=req.patient_name,
            age=req.age,
            gender=req.gender,
            allergies=", ".join(req.allergies),
            current_medications=", ".join(req.current_medications),
            symptoms=req.symptoms,
            vitals=vitals,
            agent1_output=agent1_out,
            agent2_output=agent2_out,
            agent3_output=agent3_out
        )

        return {
            "encounter_id": encounter_id,
            "patient": {
                "name": req.patient_name,
                "age": req.age,
                "gender": req.gender,
                "allergies": req.allergies,
                "current_medications": req.current_medications
            },
            "vitals": vitals,
            "agent1_symptom_analysis": agent1_out,
            "agent2_drug_check": agent2_out,
            "agent3_escalation": agent3_out,
            "final_triage_tier": agent3_out.get("final_triage_tier"),
            "responder_alert_flag": agent3_out.get("responder_alert_flag")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Triage pipeline failed: {str(e)}")

@app.get("/api/encounters")
def list_encounters(limit: int = 50):
    return db.get_all_encounters(limit=limit)

@app.get("/api/encounters/{encounter_id}")
def get_encounter(encounter_id: int):
    enc = db.get_encounter_by_id(encounter_id)
    if not enc:
        raise HTTPException(status_code=404, detail="Encounter not found")
    return enc

@app.get("/api/vitals/simulate")
def simulate_vitals(preset: str = "random"):
    """Generates realistic synthetic patient vitals for field demo testing."""
    if preset == "anaphylaxis":
        return {"heart_rate": 132, "spo2": 88, "systolic_bp": 82, "diastolic_bp": 52, "respiration_rate": 28, "temperature": 37.4}
    elif preset == "cardiac":
        return {"heart_rate": 115, "spo2": 93, "systolic_bp": 165, "diastolic_bp": 102, "respiration_rate": 24, "temperature": 36.8}
    elif preset == "sepsis":
        return {"heart_rate": 124, "spo2": 91, "systolic_bp": 86, "diastolic_bp": 50, "respiration_rate": 26, "temperature": 39.8}
    elif preset == "stable":
        return {"heart_rate": 72, "spo2": 98, "systolic_bp": 118, "diastolic_bp": 76, "respiration_rate": 15, "temperature": 36.6}
    else:
        return {
            "heart_rate": random.randint(60, 130),
            "spo2": random.randint(85, 100),
            "systolic_bp": random.randint(80, 160),
            "diastolic_bp": random.randint(50, 100),
            "respiration_rate": random.randint(12, 32),
            "temperature": round(random.uniform(36.0, 39.5), 1)
        }
