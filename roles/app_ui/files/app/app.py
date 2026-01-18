import os
import requests
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

DB_API_BASE = os.environ.get("DB_API_BASE", "http://172.31.39.132:5000")

@app.get("/")
def index():
    try:
        r = requests.get(f"{DB_API_BASE}/notes", timeout=5)
        r.raise_for_status()
        notes = r.json()
    except Exception as e:
        # Return the error in page (temporary for debugging)
        return f"<h2>DB API error</h2><pre>{e}</pre><pre>DB_API_BASE={DB_API_BASE}</pre>", 500
    return render_template("index.html", notes=notes)


@app.get("/health")
def health():
    r = requests.get(f"{DB_API_BASE}/health", timeout=5)
    return r.json()


@app.post("/add")
def add_note():
    content = (request.form.get("content") or "").strip()
    if content:
        requests.post(
            f"{DB_API_BASE}/notes",
            json={"content": content},
            timeout=5,
        )
    return redirect(url_for("index"))

@app.post("/delete/<int:note_id>")
def delete_note(note_id: int):
    requests.delete(f"{DB_API_BASE}/notes/{note_id}", timeout=5)
    return ("", 204)

@app.get("/api/note/<int:note_id>")
def api_get_note(note_id: int):
    r = requests.get(f"{DB_API_BASE}/notes/{note_id}", timeout=5)
    return jsonify(r.json()), r.status_code

@app.post("/api/note/<int:note_id>")
def api_update_note(note_id: int):
    data = request.get_json(silent=True) or {}
    content = (data.get("content") or "").strip()
    if not content:
        return jsonify({"error": "content is required"}), 400
    r = requests.put(
        f"{DB_API_BASE}/notes/{note_id}",
        json={"content": content},
        timeout=5,
    )
    return jsonify(r.json()), r.status_code
