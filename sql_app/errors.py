from fastapi import HTTPException


class UserNotFoundException(HTTPException):
    def __init__(self, status_code=404, detail="User not found"):
        super().__init__(status_code, detail)


class InvalidUserDataException(HTTPException):
    def __init__(self, status_code=400, detail="Incorrect data"):
        super().__init__(status_code, detail)
