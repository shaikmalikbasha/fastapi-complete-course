from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.helpers.jwt_utils import create_access_token
from app.helpers.utils import verify
from app.models.user_model import User
from app.schemas.user_schema import Token, UserLogin

auth_router = APIRouter(tags=["Authentication"])


@auth_router.post("/login", response_model=Token)
async def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.username == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail={"msg": "Wrong Credentials"}
        )
    if not verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail={"msg": "Wrong Credentials"}
        )

    return {
        "access_token": create_access_token(data={"user_id": user.id}),
        "token_type": "Bearer",
    }
