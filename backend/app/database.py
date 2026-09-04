"""
SQLite Local Persistence Module
Stores patient encounters, triage logs, agent pipeline records, and audit history locally.
"""

import os
import json
import sqlite3
from datetime import datetime
from typing import List, Dict, Any, Optional

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "db")
DB_PATH = os.path.join(DB_DIR, "triage_system.db")

class TriageDatabase:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_tables()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_tables(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS encounters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_name TEXT,
                age INTEGER,
                gender TEXT,
                allergies TEXT,
                current_medications TEXT,
                symptoms TEXT,
                vitals_json TEXT,
                agent1_json TEXT,
                agent2_json TEXT,
                agent3_json TEXT,
                final_triage_tier TEXT,
                responder_alert_flag INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            conn.commit()

    def save_encounter(
        self,
        patient_name: str,
        age: int,
        gender: str,
        allergies: str,
        current_medications: str,
        symptoms: str,
        vitals: dict,
        agent1_output: dict,
        agent2_output: dict,
        agent3_output: dict
    ) -> int:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO encounters (
                patient_name, age, gender, allergies, current_medications, symptoms,
                vitals_json, agent1_json, agent2_json, agent3_json,
                final_triage_tier, responder_alert_flag, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                patient_name or "Anonymous Patient",
                age,
                gender,
                allergies,
                current_medications,
                symptoms,
                json.dumps(vitals),
                json.dumps(agent1_output),
                json.dumps(agent2_output),
                json.dumps(agent3_output),
                agent3_output.get("final_triage_tier", "GREEN"),
                1 if agent3_output.get("responder_alert_flag") else 0,
                datetime.utcnow().isoformat()
            ))
            conn.commit()
            return cursor.lastrowid

    def get_all_encounters(self, limit: int = 50) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM encounters ORDER BY id DESC LIMIT ?", (limit,))
            rows = cursor.fetchall()
            encounters = []
            for row in rows:
                item = dict(row)
                item["vitals"] = json.loads(item["vitals_json"]) if item.get("vitals_json") else {}
                item["agent1_output"] = json.loads(item["agent1_json"]) if item.get("agent1_json") else {}
                item["agent2_output"] = json.loads(item["agent2_json"]) if item.get("agent2_json") else {}
                item["agent3_output"] = json.loads(item["agent3_json"]) if item.get("agent3_json") else {}
                encounters.append(item)
            return encounters

    def get_encounter_by_id(self, encounter_id: int) -> Optional[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM encounters WHERE id = ?", (encounter_id,))
            row = cursor.fetchone()
            if not row:
                return None
            item = dict(row)
            item["vitals"] = json.loads(item["vitals_json"]) if item.get("vitals_json") else {}
            item["agent1_output"] = json.loads(item["agent1_json"]) if item.get("agent1_json") else {}
            item["agent2_output"] = json.loads(item["agent2_json"]) if item.get("agent2_json") else {}
            item["agent3_output"] = json.loads(item["agent3_json"]) if item.get("agent3_json") else {}
            return item
