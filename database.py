# Simple JSON-based database handler

import json    
import os 
from typing import Any, List

class JsonDatabase:
    def __init__(self, filename: str):
        self.filename = filename
        self._ensure_file()

    def _ensure_file(self):
        if not os.path.exists(self.filename):
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump([], f, indent=4)

    def read(self) -> List[Any]:
        with open(self.filename, "r", encoding="utf-8") as f:
            return json.load(f)

    def add(self, data: dict):
        db = self.read()
        db.append(data)
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(db, f, indent=4)

    def find_by_name(self, name: str):
        db = self.read()
        for acc in db:
            if acc["name"] == name:
                return acc
        return None

    def update_account(self, updated_account):
        db = self.read()
        for i, acc in enumerate(db):
            if acc["name"] == updated_account["name"]:
                db[i] = updated_account
                break
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(db, f, indent=4)
