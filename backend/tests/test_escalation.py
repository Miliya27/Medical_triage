"""
Unit Test for Agent 3: Escalation Agent
"""

from backend.app.agents.escalation import EscalationAgent

def test_escalation_agent_red_tier():
    agent = EscalationAgent()
    
    mock_symptom_analysis = {
        "urgency_level": "RED",
        "suspected_conditions": ["Anaphylaxis"],
        "rationale": "Acute shortness of breath and hives after bee sting."
    }
    
    mock_drug_check = {
        "contraindications_found": False,
        "warnings": []
    }
    
    vitals = {
        "heart_rate": 130,
        "spo2": 88,
        "systolic_bp": 85,
        "diastolic_bp": 55,
        "respiration_rate": 30,
        "temperature": 37.2
    }
    
    result = agent.evaluate_triage(mock_symptom_analysis, mock_drug_check, vitals)
    print("Escalation Result:", result)
    
    assert result["final_triage_tier"] == "RED"
    assert result["responder_alert_flag"] is True
    assert len(result["vitals_red_flags"]) > 0
    print("✅ Escalation Agent test passed!")

if __name__ == "__main__":
    test_escalation_agent_red_tier()
