import motor.motor_asyncio
from bson import ObjectId
from decouple import config
import datetime

from .database_helper import student_helper, admin_helper, user_helper, teacher_helper

MONGO_DETAILS = config('MONGO_DETAILS')

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.webproject

# student_collection = database.get_collection('students_collection')
admin_collection = database.get_collection('admins')
teacher_collection = database.get_collection('teachers') 
user_collection = database.get_collection('users')
comment_collection = database.get_collection('comments')

async def add_admin(admin_data: dict) -> dict:
    admin = await admin_collection.insert_one(admin_data)
    new_admin = await admin_collection.find_one({"_id": admin.inserted_id})
    return admin_helper(new_admin)

async def add_user(user_data: dict) -> dict:
    user = await user_collection.insert_one(user_data)
    new_user = await user_collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user)

async def retrieve_users() -> list:
    users = []
    async for user in user_collection.find():
        users.append(user_helper(user))
    return users


async def modify_teacher_score(teacher_name:str, user:str, learned_grade:int=None, stress_grad:int=None, sweet_score:int=None):
    teacher = await teacher_collection.find_one({"name": teacher_name})
    flag=False
    ret = "User already scored "
    if teacher:
        if(user in teacher['learned_grade']['graded_user']):
            ret += "learned grade "
        else:
            teacher['learned_grade']['graded_user'].append(user)
            teacher['learned_grade']['graded']=(teacher['learned_grade']['grade']*teacher['learned_grade']['graded_user_number']+learned_grade)/(teacher['learned_grade']['graded_user_number']+1)
            # admin_collection.update_one({"name": teacher_name}, {"$set": teacher})
            flag=True
        if(user in teacher['stress_grad']['graded_user']):
            ret += "stress grade "
        else:
            teacher['stress_grad']['graded_user'].append(user)
            teacher['stress_grad']['graded']=(teacher['stress_grad']['grade']*teacher['stress_grad']['graded_user_number']+stress_grad)/(teacher['stress_grad']['graded_user_number']+1)
            # admin_collection.update_one({"name": teacher_name}, {"$set": teacher})
            flag=True
        if(user in teacher['sweet_score']['graded_user']):
            ret += "sweet score"
        else:
            teacher['sweet_score']['graded_user'].append(user)
            teacher['sweet_score']['graded']=(teacher['sweet_score']['grade']*teacher['sweet_score']['graded_user_number']+sweet_score)/(teacher['sweet_score']['graded_user_number']+1)
            # admin_collection.update_one({"name": teacher_name}, {"$set": teacher})
            flag=True
        if(flag):
            teacher_collection.update_one({"name": teacher_name}, {"$set": teacher})
            return True
        else:
            return ret
    else:
        return "Teacher not found"


async def search_teacher(name: str):
    teacher = await teacher_collection.find_one({"name": name})
    if teacher:
        return teacher_helper(teacher)

async def add_teacher(name: str):
    teacher = await teacher_collection.find_one({"name": name})
    if not teacher:
        teacher = {
            "name": name,
            "learned_grade": {
                "graded_user": [],
                "graded_user_number": 0,
                "grade": 0
            },
            "stress_grad": {
                "graded_user": [],
                "graded_user_number": 0,
                "grade": 0
            },
            "sweet_score": {
                "graded_user": [],
                "graded_user_number": 0,
                "grade": 0
            }
        }
        teacher_collection.insert_one(teacher)
        return True
    else:
        return False
        

async def update_teacher(name: str, data: dict):
    teacher = await teacher_collection.find_one({"name": name})
    if teacher:
        teacher_collection.update_one({"name": name}, {"$set": data})
        return True

async def update_teacher_comment(name: str, comment: str):
    teacher = await teacher_collection.find_one({"name": name})
    comment_collection.insert_one({"name": name, "comment": comment, "timestamp": datetime.datetime.now()})
    if teacher:
        comments = teacher['comment'].append(comment)
        teacher_collection.update_one({"name": name}, {"$set": {"comment": comments}})
        return True


# async def add_student(student_data: dict) -> dict:
#     student = await student_collection.insert_one(student_data)
#     new_student = await student_collection.find_one({"_id": student.inserted_id})
#     return student_helper(new_student)


# async def retrieve_student(id: str) -> dict:
#     student = await student_collection.find_one({"_id": ObjectId(id)})
#     if student:
#         return student_helper(student)


# async def delete_student(id: str):
#     student = await student_collection.find_one({"_id": ObjectId(id)})
#     if student:
#         await student_collection.delete_one({"_id": ObjectId(id)})
#         return True


# async def update_student_data(id: str, data: dict):
#     student = await student_collection.find_one({"_id": ObjectId(id)})
#     if student:
#         student_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
#         return True
