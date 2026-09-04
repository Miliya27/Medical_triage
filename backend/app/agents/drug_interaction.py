"""
Agent 2: Drug / Interaction Checker Agent
Cross-references patient allergies, current medications, existing conditions,
and proposed treatments against a local static formulary dataset to flag
contraindications, drug-drug interactions, and safe alternatives.
"""

import os
import json
from typing import List, Dict, Any, Optional

DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "data", "drugs", "formulary_interactions.json"
)

class DrugInteractionAgent:
    def __init__(self, data_path: str = DATA_PATH):
        self.data_path = data_path
        self.rules = []
        self._load_rules()

    def _load_rules(self):
        if os.path.exists(self.data_path):
            try:
                with open(self.data_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.rules = data.get("drug_rules", [])
            except Exception as e:
                print(f"⚠️ Error loading drug formulary: {e}")

    def check_interactions(
        self,
        proposed_drugs: List[str],
        allergies: List[str],
        current_medications: List[str],
        conditions: List[str]
    ) -> Dict[str, Any]:
        """
        Cross-reference proposed treatments with patient allergies, active meds, and conditions.
        """
        allergies_lower = [a.lower().strip() for a in allergies if a]
        current_meds_lower = [m.lower().strip() for m in current_medications if m]
        conditions_lower = [c.lower().strip() for c in conditions if c]
        proposed_lower = [p.lower().strip() for p in proposed_drugs if p]

        contraindications_found = False
        warnings = []
        recommended_alternatives = []

        for rule in self.rules:
            drug_name = rule["drug_name"]
            aliases = [a.lower() for a in rule.get("aliases", [])] + [drug_name.lower()]

            # Check if this rule's drug is being proposed or considered
            is_proposed = any(
                any(alias in prop for prop in proposed_lower) or any(prop in alias for prop in proposed_lower)
                for alias in aliases
            )

            if not is_proposed:
                continue

            # 1. Check Allergy Contraindications
            for allergy in allergies_lower:
                for contra_allergy in rule.get("contraindicated_allergies", []):
                    if contra_allergy.lower() in allergy or allergy in contra_allergy.lower():
                        contraindications_found = True
                        warnings.append({
                            "drug": drug_name,
                            "type": "ALLERGY_CONTRAINDICATION",
                            "severity": rule.get("severity", "HIGH"),
                            "conflict_item": allergy,
                            "description": f"CONTRAINDICATION: Proposed drug '{drug_name}' conflicts with patient allergy '{allergy}'. {rule.get('warning_message')}"
                        })
                        recommended_alternatives.extend(rule.get("safe_alternatives", []))

            # 2. Check Condition Contraindications
            for cond in conditions_lower:
                for contra_cond in rule.get("contraindicated_conditions", []):
                    if contra_cond.lower() in cond or cond in contra_cond.lower():
                        contraindications_found = True
                        warnings.append({
                            "drug": drug_name,
                            "type": "CONDITION_CONTRAINDICATION",
                            "severity": rule.get("severity", "HIGH"),
                            "conflict_item": cond,
                            "description": f"CONTRAINDICATION: Proposed drug '{drug_name}' is unsafe with patient condition '{cond}'. {rule.get('warning_message')}"
                        })
                        recommended_alternatives.extend(rule.get("safe_alternatives", []))

            # 3. Check Drug-Drug Interactions with Current Meds
            for med in current_meds_lower:
                for inter_drug in rule.get("interacting_drugs", []):
                    if inter_drug.lower() in med or med in inter_drug.lower():
                        contraindications_found = True
                        warnings.append({
                            "drug": drug_name,
                            "type": "DRUG_DRUG_INTERACTION",
                            "severity": rule.get("severity", "HIGH"),
                            "conflict_item": med,
                            "description": f"INTERACTION: Proposed drug '{drug_name}' interacts significantly with current medication '{med}'. {rule.get('warning_message')}"
                        })
                        recommended_alternatives.extend(rule.get("safe_alternatives", []))

        return {
            "agent_id": "DrugInteractionAgent",
            "contraindications_found": contraindications_found,
            "total_warnings": len(warnings),
            "warnings": warnings,
            "recommended_alternatives": list(set(recommended_alternatives)),
            "summary": (
                "⚠️ CONTRAINDICATIONS OR INTERACTIONS DETECTED!" if contraindications_found
                else "✅ No direct drug contraindications found in offline formulary dataset."
            )
        }
