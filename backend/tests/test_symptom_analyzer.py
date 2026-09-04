"""
Unit Test for Agent 1: Symptom Analyzer Agent
"""

from backend.app.agents.symptom_analyzer import SymptomAnalyzerAgent

def test_symptom_analyzer_anaphylaxis():
    agent = SymptomAnalyzerAgent()
    symptoms = "Patient stung by a bee 10 mins ago. Swollen lips, hives, severe difficulty breathing and wheezing."
    patient_info = {"age": 28, "gender": "Female"}
    
    result = agent.analyze(symptoms, patient_info)
    print("Symptom Analyzer Output:", result)
    
    assert "suspected_conditions" in result
    assert "urgency_level" in result
    assert result["urgency_level"] in ["RED", "YELLOW", "GREEN"]
    assert "retrieved_protocols" in result
    assert len(result["retrieved_protocols"]) > 0
    print("✅ Symptom Analyzer Agent test passed!")

if __name__ == "__main__":
    test_symptom_analyzer_anaphylaxis()
