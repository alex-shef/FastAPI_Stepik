from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from sql_app.auth import auth_router
from sql_app.errors import UserNotFoundException, InvalidUserDataException
from sql_app.routes import users, items
from sql_app.schemas import ErrorResponseModel

app = FastAPI()

app.include_router(users.router)
app.include_router(items.router)
app.include_router(auth_router)


# Добавляем пользовательный заголовок "X-ErrorHandleTime"
@app.middleware("http")
async def add_error_handle_time_header(request, call_next):
    start_time = datetime.utcnow()
    response = await call_next(request)
    end_time = datetime.utcnow()
    if (response.status_code // 100 == 4) or (response.status_code // 100 == 5):
        response.headers["X-ErrorHandleTime"] = str(end_time - start_time)
    return response


@app.exception_handler(UserNotFoundException)
async def user_not_found(request: Request, exc: ErrorResponseModel):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
    )


@app.exception_handler(InvalidUserDataException)
async def invalid_user_data(request: Request, exc: ErrorResponseModel):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
    )
