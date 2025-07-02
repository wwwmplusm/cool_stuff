"""Simple SQLite storage for user onboarding data.

Usage:
    from db import Database
    db = Database('all.db')
    db.add_goal(user_id=1, goal='Учить Python')
"""

from __future__ import annotations

import json
import sqlite3
from contextlib import closing
from typing import Any, Dict, List


class Database:
    """Wrapper around ``sqlite3`` to store user data."""

    def __init__(self, path: str) -> None:
        self.path = path
        self._init_db()

    def _init_db(self) -> None:
        with closing(sqlite3.connect(self.path)) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    area TEXT,
                    goals TEXT,
                    report_time TEXT
                )
                """
            )
            conn.commit()

    def get_user(self, user_id: int) -> Dict[str, Any]:
        with closing(sqlite3.connect(self.path)) as conn:
            row = conn.execute(
                "SELECT area, goals, report_time FROM users WHERE user_id=?",
                (user_id,),
            ).fetchone()
            if not row:
                return {"area": None, "goals": [], "report_time": None}
            area, goals_json, report_time = row
            goals = json.loads(goals_json) if goals_json else []
            return {"area": area, "goals": goals, "report_time": report_time}

    def save_user(self, user_id: int, data: Dict[str, Any]) -> None:
        with closing(sqlite3.connect(self.path)) as conn:
            conn.execute(
                (
                    "REPLACE INTO users(user_id, area, goals, report_time) "
                    "VALUES (?, ?, ?, ?)"
                ),
                (
                    user_id,
                    data.get("area"),
                    json.dumps(data.get("goals", [])),
                    data.get("report_time"),
                ),
            )
            conn.commit()

    def add_goal(self, user_id: int, goal: str) -> None:
        data = self.get_user(user_id)
        goals: List[str] = data.get("goals", [])
        goals.append(goal)
        data["goals"] = goals
        self.save_user(user_id, data)

    def remove_goal(self, user_id: int, goal: str) -> None:
        data = self.get_user(user_id)
        goals = data.get("goals", [])
        if goal in goals:
            goals.remove(goal)
        data["goals"] = goals
        self.save_user(user_id, data)

    def set_report_time(self, user_id: int, report_time: str) -> None:
        data = self.get_user(user_id)
        data["report_time"] = report_time
        self.save_user(user_id, data)
