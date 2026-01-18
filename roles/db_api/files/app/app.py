import os
import sqlite3
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

DB_PATH = os.environ.get("DB_PATH", "/opt/notesdb/data/notes.db")

def get_conn():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        conn.commit()

@app.get("/health")
def health():
    init_db()
    return jsonify({"status": "ok", "db": DB_PATH})

@app.get("/notes")
def list_notes():
    init_db()
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT id, content, created_at FROM notes ORDER BY id DESC LIMIT 100"
        ).fetchall()
    return jsonify([dict(r) for r in rows])

@app.post("/notes")
def add_note():
    init_db()
    data = request.get_json(silent=True) or {}
    content = (data.get("content") or "").strip()
    if not content:
        return jsonify({"error": "content is required"}), 400

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO notes (content, created_at) VALUES (?, ?)",
            (content, created_at),
        )
        conn.commit()

    return jsonify({"status": "created", "created_at": created_at}), 201

@app.get("/notes/<int:note_id>")
def get_note(note_id: int):
    init_db()
    with get_conn() as conn:
        row = conn.execute(
            "SELECT id, content, created_at FROM notes WHERE id = ?",
            (note_id,),
        ).fetchone()
    if row is None:
        return jsonify({"error": "not found"}), 404
    return jsonify(dict(row))

@app.put("/notes/<int:note_id>")
def update_note(note_id: int):
    init_db()
    data = request.get_json(silent=True) or {}
    content = (data.get("content") or "").strip()
    if not content:
        return jsonify({"error": "content is required"}), 400

    with get_conn() as conn:
        cur = conn.execute(
            "UPDATE notes SET content = ? WHERE id = ?",
            (content, note_id),
        )
        conn.commit()

    if cur.rowcount == 0:
        return jsonify({"error": "not found"}), 404
    return jsonify({"status": "updated", "id": note_id})


@app.delete("/notes/<int:note_id>")
def delete_note(note_id: int):
    init_db()
    with get_conn() as conn:
        cur = conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        conn.commit()
    if cur.rowcount == 0:
        return jsonify({"error": "not found"}), 404
    return jsonify({"status": "deleted", "id": note_id}), 200
