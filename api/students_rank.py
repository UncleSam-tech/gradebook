from flask import Flask, request, jsonify
from _core import students_rank as _students_rank
app = Flask(__name__)

@app.post("/")
@app.post("/api/students_rank")
def main():
    data = request.get_json(force=True) or {}
    grades = data.get("grades", {})
    if not isinstance(grades, dict):
        return jsonify({"error": "Invalid request"}), 400
    return jsonify({"students_rank": _students_rank(grades)})
