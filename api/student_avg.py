from flask import Flask, request, jsonify
from _core import student_avg as _student_avg

app = Flask(__name__)

@app.post("/")
@app.post("/api/student_avg")
def main():
    try:
        data = request.get_json(force=True) or {}
        grades = data.get("grades", {})
        student = data.get("student", "")
        if not isinstance(grades, dict) or not isinstance(student, str):
            return jsonify({"error": "Invalid request"}), 400
        return jsonify({"student": student, "student_avg": _student_avg(student, grades)})
    except Exception as e:
        return jsonify({"error": "Server error", "detail": str(e)}), 500
