"""
Agent 3: Escalation Agent
Synthesizes inputs from Agent 1 (Symptom Analyzer), Agent 2 (Drug Interaction),
and patient vitals (real/simulated) to compute a final severity tier (Red/Yellow/Green)
and decide responder escalation alerts.
"""

from typing import Dict, Any, Optional
from backend.app.llm import OfflineLLMClient

class EscalationAgent:
    def __init__(self, llm_client: Optional[OfflineLLMClient] = None):
        self.llm_client = llm_client or OfflineLLMClient()

    def evaluate_triage(
        self,
        symptom_analysis: Dict[str, Any],
        drug_check: Dict[str, Any],
        vitals: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Synthesizes Agent 1 + Agent 2 + Vitals into final severity tier.
        """
        spo2 = vitals.get("spo2", 98)
        hr = vitals.get("heart_rate", 75)
        sys_bp = vitals.get("systolic_bp", 120)
        dia_bp = vitals.get("diastolic_bp", 80)
        rr = vitals.get("respiration_rate", 16)
        temp = vitals.get("temperature", 37.0)

        # 1. Deterministic Vitals Risk Assessment
        vitals_red_flags = []
        vitals_yellow_flags = []

        if spo2 < 90:
            vitals_red_flags.append(f"Severe Hypoxia (SpO2 {spo2}%)")
        elif spo2 < 94:
            vitals_yellow_flags.append(f"Moderate Hypoxia (SpO2 {spo2}%)")

        if sys_bp < 90:
            vitals_red_flags.append(f"Hypotension / Shock Risk (Systolic BP {sys_bp} mmHg)")
        elif sys_bp > 160:
            vitals_yellow_flags.append(f"Severe Hypertension (Systolic BP {sys_bp} mmHg)")

        if hr > 120:
            vitals_red_flags.append(f"Severe Tachycardia (HR {hr} bpm)")
        elif hr < 45:
            vitals_red_flags.append(f"Severe Bradycardia (HR {hr} bpm)")
        elif hr > 100 or hr < 50:
            vitals_yellow_flags.append(f"Abnormal HR ({hr} bpm)")

        if rr > 28:
            vitals_red_flags.append(f"Severe Tachypnea (RR {rr} bpm)")
        elif rr > 22 or rr < 10:
            vitals_yellow_flags.append(f"Abnormal Respiration Rate ({rr} bpm)")

        if temp > 39.5 or temp < 35.0:
            vitals_yellow_flags.append(f"Abnormal Temperature ({temp}°C)")

        # 2. Agent 1 & Agent 2 Flags
        agent1_urgency = symptom_analysis.get("urgency_level", "GREEN")
        contraindications_found = drug_check.get("contraindications_found", False)

        # 3. Composite Triage Tier Decision Logic
        if vitals_red_flags or agent1_urgency == "RED" or contraindications_found:
            final_tier = "RED"
            tier_display = "RED - Resuscitation / Emergent"
            responder_alert = True
            base_score = 9
        elif vitals_yellow_flags or agent1_urgency == "YELLOW":
            final_tier = "YELLOW"
            tier_display = "YELLOW - Urgent / Priority"
            responder_alert = False
            base_score = 5
        else:
            final_tier = "GREEN"
            tier_display = "GREEN - Non-Urgent / Routine"
            responder_alert = False
            base_score = 2

        # Adjust score
        score_modifier = len(vitals_red_flags) * 2 + len(vitals_yellow_flags) * 1 + (2 if contraindications_found else 0)
        composite_score = min(10, base_score + score_modifier)

        # 4. LLM Clinical Synthesis Prompt
        system_prompt = "You are an emergency triage escalation coordinator."
        user_prompt = f"""EVALUATE TRIAGE CASE FOR FINAL FIELD DISPOSITION:

Agent 1 Assessment:
- Urgency: {agent1_urgency}
- Conditions: {symptom_analysis.get('suspected_conditions', [])}
- Rationale: {symptom_analysis.get('rationale', '')}

Agent 2 Drug Check:
- Contraindications Found: {contraindications_found}
- Warnings: {[w.get('description') for w in drug_check.get('warnings', [])]}

Patient Vitals:
- HR: {hr} bpm, SpO2: {spo2}%, BP: {sys_bp}/{dia_bp} mmHg, RR: {rr} /min, Temp: {temp}°C
- Red Flag Vitals: {vitals_red_flags}

Calculated Severity Tier: {final_tier}

Respond in JSON with:
{{
  "clinical_summary": "1-2 sentence narrative clinical summary combining symptoms, drug alerts, and vitals.",
  "recommended_disposition": "Immediate field emergency intervention / Queue for field doctor / Standard outpatient first-aid"
}}
"""
        synthesis = self.llm_client.generate_json(user_prompt, system_prompt=system_prompt)
        
        return {
            "agent_id": "EscalationAgent",
            "final_triage_tier": final_tier,
            "tier_display": tier_display,
            "composite_score": composite_score,
            "responder_alert_flag": responder_alert,
            "vitals_red_flags": vitals_red_flags,
            "vitals_yellow_flags": vitals_yellow_flags,
            "clinical_summary": synthesis.get("clinical_summary", f"Patient assigned {final_tier} tier based on clinical rules."),
            "recommended_disposition": synthesis.get("recommended_disposition", "Immediate evacuation" if responder_alert else "Standard protocol")
        }
