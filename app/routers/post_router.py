from typing import List

from app.database import get_db
from app.helpers.jwt_utils import get_current_user
from app.models.post_model import Post
from app.schemas.post_schema import CreateAndUpdatePost, PostResponse
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

posts_router = APIRouter(prefix="/posts", tags=["Post"])


def get_post_by_id(db: Session, post_id: int) -> Post:
    post = db.query(Post).filter(Post.id == post_id).first()

    if post:
        return post

    return None


@posts_router.get("/", response_model=List[PostResponse])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    print(posts)
    return posts


@posts_router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=PostResponse
)
async def create_post(
    post: dict = CreateAndUpdatePost,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    # new_post = Post(title=post.title, content=post.content)
    post["user_id"] = current_user.id
    new_post = Post(**post)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    # print(new_post.to_json())
    return new_post


@posts_router.get("/{post_id}", response_model=PostResponse)
async def get_posts(post_id: int, db: Session = Depends(get_db)):
    post = get_post_by_id(db, post_id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Given post with post_id:'{post_id}' is not available",
        )

    return post


@posts_router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):

    post = get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Given post with post_id:'{post_id}' is not available",
        )

    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You don't have permission to delete this post",
        )

    db.delete(post)
    db.commit()
    return "OK"


@posts_router.put("/{post_id}", status_code=status.HTTP_201_CREATED)
async def update_post(
    post_id: int, new_post: CreateAndUpdatePost, db: Session = Depends(get_db)
):
    post_query = db.query(Post).filter(Post.id == post_id)
    post = post_query.first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Given post with post_id:'{post_id}' is not available",
        )

    post_query.update({Post.title: new_post.title, Post.content: new_post.content})

    # db.add(post)
    db.commit()
    # db.refresh(post)

    # return {"msg": "New post created!", "data": post_query.first()}
    return post_query.first()
