import os, sys; sys.path.append(os.path.dirname(__file__))  # NEW
from flask import Flask, request, jsonify
from _core import subject_avg as _subject_avg

app = Flask(__name__)

@app.post("/")
@app.post("/api/subject_avg")
def main():
    try:
        data = request.get_json(force=True) or {}
        grades  = data.get("grades", {})
        subject = data.get("subject", "")
        student = data.get("student", "")
        if not isinstance(grades, dict) or not isinstance(subject, str) or not isinstance(student, str):
            return jsonify({"error": "Invalid request"}), 400
        return jsonify({
            "student": student,
            "subject": subject,
            "subject_avg": _subject_avg(subject, grades, student)
        })
    except Exception as e:
        return jsonify({"error": "Server error", "detail": str(e)}), 500
