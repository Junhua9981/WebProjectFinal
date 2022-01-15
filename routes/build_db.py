from fastapi import Body, APIRouter
import json
import motor.motor_asyncio
from bson import ObjectId
from decouple import config
# from database.tools import v_code
# import tools


MONGO_DETAILS = config('MONGO_DETAILS')

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.webproject

# student_collection = database.get_collection('students_collection')
teacher_collection = database.get_collection('teachers') 
router = APIRouter()

SECRET = config('secret')

@router.post("/", response_description="YA")
async def build_db(secret: str = Body(...)):
    if(secret == SECRET):
        data = []
        with open(r'routes\result.json', 'r', encoding="UTF-8") as obj:
            data = json.load(obj)
        for te in data:
            teacher = {
                    "name": te.get('name'),
                    "department": te.get('department'),
                    "teaching_subject": te.get('classes'),
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
        return {
            "status": "success",
            "code": 200
        }
    else:
        return {
            "status": "fail",
            "code": 400
        }