from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr

from app.schemas.post_schema import PostAlone


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[int]


class UserLogin(BaseModel):
    username: EmailStr
    password: str


class UserBase(BaseModel):
    username: str
    created_at: datetime
    is_active: Optional[bool] = True


class CreateAndUpdateUser(UserBase):
    username: EmailStr
    password: str


# class UserAlone(UserBase):
#     id: int
#     created_at: datetime

# class Config:
#     orm_mode = True


class UserResponse(UserBase):
    id: int
    username: EmailStr
    created_at: datetime
    posts: List[PostAlone] = []

    class Config:
        orm_mode = True
