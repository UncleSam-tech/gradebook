# api/_core.py

def _avg(nums):
    return sum(nums) / len(nums) if nums else None

def student_avg(student, grades):
    if student not in grades or not grades[student]:
        return None
    per_subject_avgs = []
    for grade_list in grades[student].values():
        nums = [float(g) for g in grade_list]
        a = _avg(nums)
        if a is not None:
            per_subject_avgs.append(a)
    return _avg(per_subject_avgs) if per_subject_avgs else None

def subject_avg(subject, grades, student):
    if student not in grades:
        return None
    grade_list = grades[student].get(subject, [])
    nums = [float(g) for g in grade_list]
    return _avg(nums) if nums else None

def students_rank(grades):
    rank = []
    for s in grades.keys():
        a = student_avg(s, grades)
        if a is not None:
            rank.append((s, a))
    rank.sort(key=lambda x: x[1], reverse=True)
    return rank

def full_student_data(grades, student):
    if student not in grades:
        return None
    student_grades = grades[student]
    subject_averages = {}
    for subject, grade_list in student_grades.items():
        nums = [float(g) for g in grade_list]
        if nums:
            subject_averages[subject] = _avg(nums)
    overall_avg = student_avg(student, grades)
    return {"student": student, "subject_averages": subject_averages, "overall_average": overall_avg}
