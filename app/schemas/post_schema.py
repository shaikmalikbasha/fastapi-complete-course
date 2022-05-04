from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str
    is_published: Optional[bool] = True


class CreateAndUpdatePost(PostBase):
    pass


class PostAlone(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class PostResponse(PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: Any = {}

    class Config:
        orm_mode = True
