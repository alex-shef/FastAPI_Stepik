from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict


class ItemBase(BaseModel):
    title: str
    description: str | None = None
    created_at: datetime
    completed: bool = False


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    title: str | None = None  # Атрибуты могут быть None, чтобы указать, что они не обновляются
    description: str | None = None
    completed: bool | None = None


class Item(ItemBase):
    id: int
    owner_id: int

    # class Config:
    #     from_attributes = True
    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    email: EmailStr
    username: str
    role: Optional[str] = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    # class Config:
    #     from_attributes = True
    model_config = ConfigDict(from_attributes=True)


class ErrorResponseModel(BaseModel):
    status_code: int
    detail: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
