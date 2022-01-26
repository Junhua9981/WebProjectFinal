from ast import Str
import motor.motor_asyncio
from bson import ObjectId
from decouple import config
import datetime
from database.tools import v_code
from database.mail import send_mail
# import tools

from models.teacher import TeacherModel, TeacherCommentModel
from .database_helper import student_helper, admin_helper, teacher_comment_helper, user_helper, teacher_helper, comment_helper, teacher_name_helper

MONGO_DETAILS = config('MONGO_DETAILS')

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.webproject

teacher_collection = database.get_collection('teachers') 
user_collection = database.get_collection('users')
comment_collection = database.get_collection('comments')

async def login_token(email:str , token: str):
    user = await user_collection.find_one({"email": email})
    if user:
        a = await user_collection.update_one({"email": email}, {"$set": {"token": token}})
        return True
    else:
        return False

async def save_courseTable(email: str, courseTable: str):
    user = await user_collection.find_one({"email": email})
    if user:
        await user_collection.update_one({"email": email}, {"$set": {"courseTable": courseTable}})
        return True
    else:
        return False

# async def add_admin(admin_data: dict) -> dict:
#     admin = await admin_collection.insert_one(admin_data)
#     new_admin = await admin_collection.find_one({"_id": admin.inserted_id})
#     return admin_helper(new_admin)

async def send_activate_mail(email: Str):
    activateCode = v_code()
    await send_mail(email, "Here is your activate code" ,activateCode)
    user = await user_collection.find_one({"email": email})
    if user :
        await user_collection.update_one({"email": email}, {"$set": {"activateCode": activateCode}})
        return True
    else :
        user = await user_collection.insert_one({"email": email, "activateCode": activateCode})
        return True
    return False

async def add_user(user_data: dict) -> dict:
    user_collection.update_one({"email": user_data['email']}, {"$set": user_data})
    new_user = await user_collection.find_one({"email": user_data['email']})
    return user_helper(new_user)

async def retrieve_users() -> list:
    users = []
    async for user in user_collection.find():
        users.append(user_helper(user))
    return {
        "email":users,
        "status": "success",
        "code": 200
    }


async def modify_teacher_score(teacher_name:str, user:str, learned_grade:float=None, stress_grade:float=None, sweet_score:float=None):
    teacher = await teacher_collection.find_one({"name": teacher_name})
    flag=False
    ret = "User already scored "
    if teacher:
        if(user in teacher['learned_grade']['graded_user']):
            ret += "learned grade "
        else:
            if(learned_grade>=0 and learned_grade<=5):
                teacher['learned_grade']['graded_user'].append(user)
                teacher['learned_grade']['grade']=(teacher['learned_grade']['grade']*teacher['learned_grade']['graded_user_number']+learned_grade)/(teacher['learned_grade']['graded_user_number']+1)
                teacher['learned_grade']['graded_user_number']+=1
            # admin_collection.update_one({"name": teacher_name}, {"$set": teacher})
                flag=True
        if(user in teacher['stress_grade']['graded_user']):
            ret += "stress grade "
        else:
            if(stress_grade>=0 and stress_grade<=5):
                teacher['stress_grade']['graded_user'].append(user)
                teacher['stress_grade']['grade']=(teacher['stress_grade']['grade']*teacher['stress_grade']['graded_user_number']+stress_grade)/(teacher['stress_grade']['graded_user_number']+1)
                teacher['stress_grade']['graded_user_number']+=1
                # admin_collection.update_one({"name": teacher_name}, {"$set": teacher})
                flag=True
        if(user in teacher['sweet_score']['graded_user']):
            ret += "sweet score"
        else:
            if(sweet_score>=0 and sweet_score<=5):
                teacher['sweet_score']['graded_user'].append(user)
                teacher['sweet_score']['grade']=(teacher['sweet_score']['grade']*teacher['sweet_score']['graded_user_number']+sweet_score)/(teacher['sweet_score']['graded_user_number']+1)
                teacher['sweet_score']['graded_user_number']+=1
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
        ret = {
            "name": teacher['name'],
            "department": teacher['department'],
            "teaching_subject": teacher['teaching_subject'],
            "learned_grade": teacher['learned_grade']['grade'] if teacher['learned_grade']['graded_user_number'] else -1,
            "learned_graded_user_number": teacher['learned_grade']['graded_user_number'] if teacher['learned_grade']['graded_user_number'] else -1,
            "stress_grade": teacher['stress_grade']['grade'] if teacher['stress_grade']['graded_user_number'] else -1,
            "stress_graded_user_number": teacher['stress_grade']['graded_user_number'] if teacher['stress_grade']['graded_user_number'] else -1,
            "sweet_score": teacher['sweet_score']['grade'] if teacher['sweet_score']['graded_user_number'] else -1,
            "sweet_graded_user_number": teacher['sweet_score']['graded_user_number'] if teacher['sweet_score']['graded_user_number'] else -1,
        }
        return teacher_helper(ret)

async def add_teacher(name: str):
    teacher = await teacher_collection.find_one({"name": name})
    if not teacher:
        teacher = {
            "name": name,
            "department": "",
            "teaching_subject": "",
            "learned_grade": {
                "graded_user": [],
                "graded_user_number": 0,
                "grade": 0
            },
            "stress_grade": {
                "graded_user": [],
                "graded_user_number": 0,
                "grade": 0
            },
            "sweet_score": {
                "graded_user": [],
                "graded_user_number": 0,
                "grade": 0
            },
            "comments": []
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

async def update_teacher_comment(name: str, username:str, comment: str):
    teacher = await teacher_collection.find_one({"name": name})
    if teacher:
        for user in teacher['comments']:
            if username==user['name']:
                return False
        comment_collection.insert_one({"name": username, "comment": comment, "timestamp": datetime.datetime.now(), "teacher": name})
        if( teacher['comments'] ):
            comments = teacher['comments']
            comments.append({"name": username, "comment": comment, "timestamp": datetime.datetime.now()})
        else:
            comments = [{"name": username, "comment": comment, "timestamp": datetime.datetime.now()}]
        teacher_collection.update_one({"name": name}, {"$set": {"comments": comments}})
        return True
    else:
        return False

async def retrieve_teacher_comment(name: str):
    teacher = await teacher_collection.find_one({"name": name})
    if teacher:
        # ret = []
        # for comment in teacher['comments']:
        #     ret.append({"comment": comment['comment'], "timestamp": comment['timestamp']})
        # return ret 
        return teacher_comment_helper(teacher['comments']) if len(teacher['comments'])>0 else []

async def retrieve_recent_comment():
    comments = []
    async for comment in comment_collection.find().sort("timestamp", -1).limit(10):
        comments.append(comment_helper(comment))
    return comments


async def retrieve_teacher() -> list:
    teachers = []
    async for teacher in teacher_collection.find():
        teachers.append(teacher_name_helper(teacher))
    return {
        'teachers':teachers
    }
