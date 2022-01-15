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
        "id": str(user['_id']),
        "name": user['name'],
        "email": user['email'],
    }

def teacher_helper(teacher) -> dict:
    return {
        "name": teacher['name'],
        "department": teacher['department'],
        "teaching_subject": teacher['teaching_subject'],
        "learned_grade": teacher['learned_grade'],
        "stress_grad": teacher['stress_grad'],
        "sweet_score": teacher['sweet_score'],
    }

def teacher_comment_helper(teacher) -> dict:
    return {
        "comment": teacher['comment'],
    }