from typing import Annotated

from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session

from sql_app import schemas, crud
from sql_app.auth import get_current_user, get_user_by_username
from sql_app.database import get_db

router = APIRouter()


@router.post("/create_first_admin", response_model=schemas.User)
async def create_first_admin(user: schemas.UserCreate, db: Session = Depends(get_db)):
    users = await crud.get_users(skip=0, limit=100, db=db)
    if users:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Admin already exists")
    return await crud.create_user(user=user, db=db)


@router.post("/users/", response_model=schemas.User, tags=["admin"])
async def create_user(current_user: Annotated[schemas.User, Depends(get_current_user)],
                      user: schemas.UserCreate, db: Session = Depends(get_db)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
    db_user = await crud.get_user_by_email(email=user.email, db=db)
    if db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    db_user = await get_user_by_username(username=user.username, db=db)
    if db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already registered")
    return await crud.create_user(user=user, db=db)


@router.get("/users/", response_model=list[schemas.User], tags=["admin"])
async def get_users(current_user: Annotated[schemas.User, Depends(get_current_user)],
                    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
    users = await crud.get_users(skip=skip, limit=limit, db=db)
    return users


@router.get("/users/{user_id}", response_model=schemas.User, tags=["admin"])
async def get_user(current_user: Annotated[schemas.User, Depends(get_current_user)],
                   user_id: int, db: Session = Depends(get_db)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
    db_user = await crud.get_user_by_id(user_id=user_id, db=db)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user
