def ResponseModel(data, message):
    return {
        "data": [
            data
        ],
        "code": 200,
        "message": message,
    }

def CommentResposeModel(comment):
    return {
        "comment": comment
    }

def SuccessResponseModel(status, code, message):
    return {
        "status": status,
        "code": code,
        "message": message
    }

def ErrorResponseModel(error, code, message):
    return {
        "status": error,
        "code": code,
        "message": message
    }

def ResModel(status, code, message):
    return {
        "status": status,
        "code": code,
        "message": message,
    }

def LoginFailResModel(status, code, message):
    return {
        "status": status,
        "code": code,
        "message": message
    }

def LoginSucResModel(status, code, message, tk):
    return {
        "status": status,
        "code": code,
        "message": message,
        "token": tk
    }