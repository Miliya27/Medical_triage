"""
Integration Test for FastAPI Triage Pipeline API
"""

from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    print("✅ Health check API passed!")

def test_simulate_vitals():
    response = client.get("/api/vitals/simulate?preset=anaphylaxis")
    assert response.status_code == 200
    vitals = response.json()
    assert vitals["spo2"] == 88
    assert vitals["heart_rate"] == 132
    print("✅ Simulated vitals API passed!")

def test_full_triage_pipeline_api():
    payload = {
        "patient_name": "Test Patient John",
        "age": 45,
        "gender": "Male",
        "symptoms": "Severe crushing chest pain radiating to left arm with shortness of breath and cold sweat.",
        "allergies": ["Penicillin"],
        "current_medications": ["Sildenafil"],
        "proposed_treatments": ["Nitroglycerin", "Aspirin"],
        "vitals": {
            "heart_rate": 118,
            "spo2": 92,
            "systolic_bp": 88,
            "diastolic_bp": 58,
            "respiration_rate": 26,
            "temperature": 36.9
        }
    }
    
    response = client.post("/api/triage/run", json=payload)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    data = response.json()
    
    assert "encounter_id" in data
    assert data["final_triage_tier"] == "RED"
    assert data["responder_alert_flag"] is True
    assert "agent1_symptom_analysis" in data
    assert "agent2_drug_check" in data
    assert "agent3_escalation" in data
    
    # Check that drug interaction warning for Nitroglycerin + Sildenafil was caught by Agent 2
    drug_check = data["agent2_drug_check"]
    assert drug_check["contraindications_found"] is True
    
    print(f"✅ Full Triage API Test Passed! Encounter ID: {data['encounter_id']}")

def test_get_encounters_list():
    response = client.get("/api/encounters")
    assert response.status_code == 200
    encounters = response.json()
    assert len(encounters) > 0
    print(f"✅ List encounters API passed! Total stored: {len(encounters)}")

if __name__ == "__main__":
    test_health_check()
    test_simulate_vitals()
    test_full_triage_pipeline_api()
    test_get_encounters_list()
