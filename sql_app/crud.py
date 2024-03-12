from sqlalchemy.orm import Session

from sql_app import models
from sql_app import schemas
from sql_app.auth import get_password_hash


async def create_user(user: schemas.UserCreate, db: Session):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, username=user.username, hashed_password=hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


async def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


async def get_user_by_id(user_id: int, db: Session):
    return db.query(models.User).filter(models.User.id == user_id).first()


async def get_user_by_email(email: str, db: Session):
    return db.query(models.User).filter(models.User.email == email).first()


async def create_item(user_id: int, item_create: schemas.ItemCreate, db: Session):
    db_item = models.Item(**item_create.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


async def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


async def get_item(item_id: int, db: Session):
    return db.query(models.Item).filter(models.Item.id == item_id).first()


async def update_item(item_id: int, item_update: schemas.ItemUpdate, db: Session):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item:
        for var, value in vars(item_update).items():
            setattr(db_item, var, value)  # Обновляем атрибуты элемента из данных обновления
        db.commit()
        db.refresh(db_item)
    return db_item


# Удаление элемента
async def delete_item(item_id: int, db: Session):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item
