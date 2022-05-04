from typing import List

from app.database import get_db
from app.helpers.utils import get_hash_password
from app.models.user_model import User
from app.schemas.user_schema import CreateAndUpdateUser, UserResponse
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

user_router = APIRouter(prefix="/users", tags=["Users"])

# admin_required= None


@user_router.get("/", response_model=List[UserResponse])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()

    print(f"UsersQuery: {users}")

    return users


@user_router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_post(user: CreateAndUpdateUser, db: Session = Depends(get_db)):
    user.password = get_hash_password(user.password)
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    # print(new_post.to_json())
    return new_user


@user_router.get("/{id}", response_model=UserResponse)
async def get_users(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"msg": f"Given user with user_id:'{id}' is not available"},
        )

    return user
