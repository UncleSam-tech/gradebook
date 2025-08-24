from flask import Flask, request, jsonify
from _core import full_student_data as _full_student_data

app = Flask(__name__)

@app.pos("/")
def main():
    data = request.get_json(force=True) or {}
    grades = data.get("grades", {})
    student = data.get("student", "")
    if not isinstance(grades, dict) or not isinstance(student, str):
        return jsonify({"error": "Invalid request"}), 400
    return jsonify({"full_student_data": _full_student_data(grades, student)})
