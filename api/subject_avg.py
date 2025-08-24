from flask import Flask, request, jsonify
from _core import subject_avg as _subject_avg
app = Flask(__name__)

@app.post("/", defaults={"_": ""})
@app.post("/api/subject_avg")
def main():
    data = request.get_json(force=True) or {}
    grades = data.get("grades", {})
    subject = data.get("subject", "")
    student = data.get("student", "")
    if not isinstance(grades, dict) or not isinstance(subject, str) or not isinstance(student, str):
        return jsonify({"error": "Invalid request"}), 400
    return jsonify({"student": student, "subject": subject,
                    "subject_avg": _subject_avg(subject, grades, student)})
