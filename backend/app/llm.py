"""
Offline LLM Client Module
Provides an interface to locally running Ollama models (llama3.2:3b / phi3:mini)
with automatic fallback synthesis for reliable offline medical triage execution.
"""

import json
import urllib.request
import urllib.error
import re
from typing import Dict, Any, Optional

OLLAMA_BASE_URL = "http://localhost:11434"

class MockOllamaEngine:
    """Fallback engine for offline operation when Ollama daemon is not running."""
    
    @staticmethod
    def synthesize_symptom_analysis(prompt: str, retrieved_context: str = "") -> Dict[str, Any]:
        prompt_lower = prompt.lower()
        
        # Severe / Anaphylactic / Cardiac symptoms
        if any(term in prompt_lower for term in ["sting", "hives", "shortness of breath", "wheezing", "chest pain", "bleeding", "unconscious", "stroke"]):
            if "sting" in prompt_lower or "hives" in prompt_lower:
                return {
                    "suspected_conditions": ["Anaphylaxis", "Severe Allergic Reaction", "Airway Compromise"],
                    "primary_concerns": ["Potential airway edema and rapid hemodynamic collapse"],
                    "urgency_level": "RED",
                    "triage_category": "Immediate / Resuscitation",
                    "rationale": "Acute onset of multi-system involvement (skin + respiratory) following allergen exposure.",
                    "recommended_actions": [
                        "Administer IM Epinephrine 0.3mg immediately if available",
                        "Maintain patent airway and position patient supine with feet elevated",
                        "Prepare for high-flow oxygen and emergency evacuation"
                    ]
                }
            elif "chest pain" in prompt_lower or "heart" in prompt_lower:
                return {
                    "suspected_conditions": ["Acute Coronary Syndrome", "Myocardial Infarction", "Angina"],
                    "primary_concerns": ["Cardiac ischemia and malignant arrhythmia"],
                    "urgency_level": "RED",
                    "triage_category": "Immediate",
                    "rationale": "Chest pain with potential radiation or cardiac stress indicators.",
                    "recommended_actions": [
                        "Administer Aspirin 325mg chewable if no contraindications",
                        "Keep patient strictly at rest in semi-Fowler position",
                        "Continuous ECG and vitals monitoring"
                    ]
                }
            else:
                return {
                    "suspected_conditions": ["Severe Acute Illness / Trauma", "Hypoxia / Shock Risk"],
                    "primary_concerns": ["Vital sign instability or severe pain"],
                    "urgency_level": "RED",
                    "triage_category": "Immediate",
                    "rationale": "High-risk red-flag symptoms present requiring immediate clinical evaluation.",
                    "recommended_actions": [
                        "Stabilize ABCs (Airway, Breathing, Circulation)",
                        "Establish IV access and provide immediate supportive care",
                        "Priority evacuation to high-level field facility"
                    ]
                }
        # Moderate / Yellow tier symptoms
        elif any(term in prompt_lower for term in ["fever", "cough", "vomiting", "pain", "abdominal", "fracture", "diarrhea"]):
            return {
                "suspected_conditions": ["Acute Gastroenteritis", "Localized Infection", "Moderate Musculoskeletal Injury"],
                "primary_concerns": ["Dehydration, pain control, or infection progression"],
                "urgency_level": "YELLOW",
                "triage_category": "Urgent",
                "rationale": "Significant clinical distress without immediate life-threatening airway/breathing failure.",
                "recommended_actions": [
                    "Initiate oral rehydration solution (ORS)",
                    "Administer antipyretic or mild analgesic if indicated",
                    "Re-evaluate vitals every 30 minutes"
                ]
            }
        # Mild / Green tier symptoms
        else:
            return {
                "suspected_conditions": ["Minor Abrasions / Cut", "Mild Upper Respiratory Tract Infection", "Routine Fatigue"],
                "primary_concerns": ["Symptomatic relief and infection prevention"],
                "urgency_level": "GREEN",
                "triage_category": "Non-Urgent / Minor",
                "rationale": "Stable vitals and isolated mild symptoms without red flags.",
                "recommended_actions": [
                    "Clean and bandage minor wounds with standard antiseptic",
                    "Advise rest, fluid intake, and self-monitoring",
                    "Re-assess if symptoms worsen"
                ]
            }

    @staticmethod
    def synthesize_escalation(symptom_analysis: dict, drug_check: dict, vitals: dict) -> Dict[str, Any]:
        spo2 = vitals.get("spo2", 98)
        hr = vitals.get("heart_rate", 75)
        sys_bp = vitals.get("systolic_bp", 120)
        
        urgency = symptom_analysis.get("urgency_level", "GREEN")
        contraindications = drug_check.get("contraindications_found", False)
        
        # Determine final severity tier
        if spo2 < 90 or sys_bp < 90 or hr > 120 or urgency == "RED" or contraindications:
            tier = "RED"
            tier_name = "Emergent / Resuscitation"
            alert = True
        elif spo2 < 94 or sys_bp > 140 or hr > 100 or urgency == "YELLOW":
            tier = "YELLOW"
            tier_name = "Urgent / Priority"
            alert = False
        else:
            tier = "GREEN"
            tier_name = "Non-Urgent / Routine"
            alert = False
            
        return {
            "final_triage_tier": tier,
            "tier_display": tier_name,
            "responder_alert_flag": alert,
            "composite_score": 9 if tier == "RED" else (5 if tier == "YELLOW" else 2),
            "summary_rationale": f"Calculated severity tier {tier}. Vitals: SpO2={spo2}%, HR={hr}bpm, BP={sys_bp} mmHg. Contraindications: {contraindications}.",
            "recommended_next_step": "Immediate Field Resuscitation & Evacuation Queue" if alert else "Observation & Re-eval in 1 hour"
        }


class OfflineLLMClient:
    def __init__(self, default_model: str = "llama3.2:3b", base_url: str = OLLAMA_BASE_URL):
        self.default_model = default_model
        self.base_url = base_url

    def is_ollama_available(self) -> bool:
        try:
            req = urllib.request.Request(f"{self.base_url}/api/tags")
            with urllib.request.urlopen(req, timeout=2) as resp:
                return resp.status == 200
        except Exception:
            return False

    def generate_json(self, prompt: str, system_prompt: str = "", model_name: Optional[str] = None) -> Dict[str, Any]:
        target_model = model_name or self.default_model
        
        if self.is_ollama_available():
            full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            payload = {
                "model": target_model,
                "prompt": full_prompt,
                "stream": False,
                "format": "json"
            }
            try:
                data = json.dumps(payload).encode("utf-8")
                req = urllib.request.Request(
                    f"{self.base_url}/api/generate",
                    data=data,
                    headers={"Content-Type": "application/json"}
                )
                with urllib.request.urlopen(req, timeout=30) as resp:
                    res = json.loads(resp.read().decode())
                    text_resp = res.get("response", "")
                    return json.loads(text_resp)
            except Exception as e:
                print(f"⚠️ Ollama error: {e}. Falling back to offline engine.")
        
        # Fallback to local deterministic medical engine
        return MockOllamaEngine.synthesize_symptom_analysis(prompt)
