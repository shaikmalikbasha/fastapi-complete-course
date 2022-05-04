from fastapi import FastAPI

from .database import Base, engine
from app.routers import user_router, post_router
from app.auth import auth_router


Base.metadata.create_all(engine)

app = FastAPI(
    title="FastAPI Application",
    description="Posts and Users CRUD App",
    version="0.0.1",
    contact={"name": "Shaik Malik Basha", "email": "shaikmalikbasha@example.com"},
    license_info={"name": "MIT"},
)


app.include_router(auth_router)
app.include_router(user_router.user_router)
app.include_router(post_router.posts_router)

# @app.on_event("startup")
# def create_tables():
#     print("I am always executing first...")
#     Base.metadata.create_all(engine)
#     print("We can create the tables here")
