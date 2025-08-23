# api/index.py
from flask import Flask, request, jsonify

app = Flask(__name__)

# ----------------------
# Core operations
# ----------------------
def _avg(nums):
    return sum(nums) / len(nums) if nums else None

def student_avg(student, grades):
    """
    grades: { student: { subject: [grades...] } }
    returns overall average across the student's subjects (average of subject averages)
    """
    if student not in grades or not grades[student]:
        return None

    per_subject_avgs = []
    for grade_list in grades[student].values():
        # grade_list is a list of numbers/strings
        nums = [float(g) for g in grade_list]
        a = _avg(nums)
        if a is not None:
            per_subject_avgs.append(a)

    return _avg(per_subject_avgs) if per_subject_avgs else None

def subject_avg(subject, grades, student):
    """
    returns the average for a specific subject for a given student
    """
    if student not in grades:
        return None
    grade_list = grades[student].get(subject, [])
    nums = [float(g) for g in grade_list]
    return _avg(nums) if nums else None

def students_rank(grades):
    """
    returns list of tuples (student, average) sorted desc by average
    """
    rank = []
    for s in grades.keys():
        a = student_avg(s, grades)
        if a is not None:
            rank.append((s, a))
    rank.sort(key=lambda x: x[1], reverse=True)
    return rank

def full_student_data(grades, student):
    """
    returns per-subject averages and overall average for a student
    """
    if student not in grades:
        return None

    student_grades = grades[student]
    subject_averages = {}

    for subject, grade_list in student_grades.items():
        nums = [float(g) for g in grade_list]
        if nums:
            subject_averages[subject] = _avg(nums)

    overall_avg = student_avg(student, grades)
    return {
        "student": student,
        "subject_averages": subject_averages,
        "overall_average": overall_avg
    }

# ----------------------
# API Endpoints
# ----------------------
@app.get("/api/ping")
def ping():
    return jsonify({"ok": True})

@app.post("/api/student-avg")
def api_student_avg():
    data = request.get_json(force=True) or {}
    grades = data.get("grades", {})
    student = data.get("student", "")
    if not isinstance(grades, dict) or not isinstance(student, str):
        return jsonify({"error": "Invalid request"}), 400
    return jsonify({"student": student, "student_avg": student_avg(student, grades)})

@app.post("/api/subject-avg")
def api_subject_avg():
    data = request.get_json(force=True) or {}
    grades = data.get("grades", {})
    subject = data.get("subject", "")
    student = data.get("student", "")
    if not isinstance(grades, dict) or not isinstance(subject, str) or not isinstance(student, str):
        return jsonify({"error": "Invalid request"}), 400
    return jsonify({
        "student": student,
        "subject": subject,
        "subject_avg": subject_avg(subject, grades, student)
    })

@app.post("/api/students-rank")
def api_students_rank():
    data = request.get_json(force=True) or {}
    grades = data.get("grades", {})
    if not isinstance(grades, dict):
        return jsonify({"error": "Invalid request"}), 400
    return jsonify({"students_rank": students_rank(grades)})

@app.post("/api/full-student-data")
def api_full_student_data():
    data = request.get_json(force=True) or {}
    grades = data.get("grades", {})
    student = data.get("student", "")
    if not isinstance(grades, dict) or not isinstance(student, str):
        return jsonify({"error": "Invalid request"}), 400
    return jsonify({"full_student_data": full_student_data(grades, student)})
