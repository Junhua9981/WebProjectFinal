def student_helper(student) -> dict:
    return {
        "id": str(student['_id']),
        "fullname": student['fullname'],
        "email": student['email'],
        "course_of_study": student['course_of_study'],
        "year": student['year'],
        "GPA": student['gpa']
    }

def admin_helper(admin) -> dict:
    return {
        "name": admin['name'],
    }

def user_helper(user) -> dict:
    return {
        "email": user['email'],
    }

def teacher_helper(teacher) -> dict:
    return {
        "name": teacher['name'],
        "department": teacher['department'],
        "teaching_subject": teacher['teaching_subject'],
        "learned_grade": teacher['learned_grade'],
        "stress_grade": teacher['stress_grade'],
        "sweet_score": teacher['sweet_score'],
    }

def teacher_name_helper(teacher) -> dict:
    return {
        "name": teacher['name'],
    }

def teacher_comment_helper(teacher) -> list:
    ret = []
    for comment in teacher:
        ret.append({"comment": comment['comment'], "timestamp": comment['timestamp']})
    return ret

def comment_helper(comment) -> dict:
    return {
        "comment": comment['comment'],
        "timestamp": comment['timestamp'],
        "teacher": comment['teacher'],
    }