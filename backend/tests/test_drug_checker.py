"""
Unit Test for Agent 2: Drug Interaction Checker Agent
"""

from backend.app.agents.drug_interaction import DrugInteractionAgent

def test_drug_interaction_checker():
    agent = DrugInteractionAgent()
    
    # Test case: Nitroglycerin proposed for patient on Sildenafil
    result1 = agent.check_interactions(
        proposed_drugs=["Nitroglycerin"],
        allergies=[],
        current_medications=["Sildenafil"],
        conditions=["Chest Pain"]
    )
    print("Test 1 Result:", result1)
    assert result1["contraindications_found"] is True
    assert result1["warnings"][0]["type"] == "DRUG_DRUG_INTERACTION"

    # Test case: Amoxicillin proposed for patient allergic to Penicillin
    result2 = agent.check_interactions(
        proposed_drugs=["Amoxicillin"],
        allergies=["Penicillin allergy"],
        current_medications=[],
        conditions=["Fever"]
    )
    print("Test 2 Result:", result2)
    assert result2["contraindications_found"] is True
    assert result2["warnings"][0]["type"] == "ALLERGY_CONTRAINDICATION"
    assert len(result2["recommended_alternatives"]) > 0

    print("✅ Drug Interaction Agent tests passed!")

if __name__ == "__main__":
    test_drug_interaction_checker()
