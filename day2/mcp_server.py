from fastmcp import FastMCP
import sqlite3
import json
from datetime import datetime

mcp = FastMCP("tutoring-tools")

def get_db():
    conn = sqlite3.connect("tutoring.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT,
            topic TEXT,
            problem TEXT,
            score REAL,
            attempts INTEGER,
            hints_used INTEGER,
            timestamp TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS problems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT,
            problem TEXT,
            answer TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    return conn

@mcp.tool()
def save_score(student_id: str, topic: str, problem: str, score: float, attempts: int, hints_used: int) -> str:
    conn = get_db()
    conn.execute(
        "INSERT INTO scores (student_id, topic, problem, score, attempts, hints_used, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (student_id, topic, problem, score, attempts, hints_used, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()
    return f"Score saved for student {student_id}"

@mcp.tool()
def get_student_history(student_id: str) -> str:
    conn = get_db()
    cursor = conn.execute(
        "SELECT topic, problem, score, attempts, hints_used, timestamp FROM scores WHERE student_id = ?",
        (student_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        return "No history found"
    history = [
        {"topic": r[0], "problem": r[1], "score": r[2], "attempts": r[3], "hints_used": r[4], "timestamp": r[5]}
        for r in rows
    ]
    return json.dumps(history)

@mcp.tool()
def save_problem(topic: str, problem: str, answer: str) -> str:
    conn = get_db()
    conn.execute(
        "INSERT INTO problems (topic, problem, answer, timestamp) VALUES (?, ?, ?, ?)",
        (topic, problem, answer, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()
    return f"Problem saved for topic {topic}"

@mcp.tool()
def get_problems_by_topic(topic: str) -> str:
    conn = get_db()
    cursor = conn.execute(
        "SELECT problem, answer FROM problems WHERE topic = ?",
        (topic,)
    )
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        return "No problems found"
    problems = [{"problem": r[0], "answer": r[1]} for r in rows]
    return json.dumps(problems)

if __name__ == "__main__":
    mcp.run()
    