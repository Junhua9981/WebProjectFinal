def ResponseModel(data, message):
    return {
        "data": [
            data
        ],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {
        "error": error,
        "code": code,
        "message": message
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