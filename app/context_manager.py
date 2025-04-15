from datetime import datetime
from typing import Dict, Any
import json
from pathlib import Path


class ContextManager:
    def __init__(self):
        self.sessions = {}
        self.data_path = Path("data/session_data.json")
        self.load_sessions()

    def load_sessions(self):
        if self.data_path.exists():
            with open(self.data_path, "r") as f:
                self.sessions = json.load(f)

    def save_sessions(self):
        with open(self.data_path, "w") as f:
            json.dump(self.sessions, f)

    def get_context(self, session_id: str) -> Dict[str, Any]:
        """Get or create session context"""
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "conversation_history": [],
                "preferences": {},
                "state": "initial"
            }
            self.save_sessions()
        return self.sessions[session_id]

    def update_context(self, session_id: str, updates: Dict[str, Any]):
        """Update session context"""
        if session_id in self.sessions:
            self.sessions[session_id].update(updates)
            self.sessions[session_id]["updated_at"] = datetime.now().isoformat()
            self.save_sessions()