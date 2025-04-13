from typing import Annotated
from fastapi import APIRouter, Depends
from app.posts.crud import PostsDAO
from app.users.dependencies import get_current_is_user
from app.users.schemas import UsersAuthorizationSchema
from app.posts.schemas import PostsSchemas

router = APIRouter(prefix="/users", tags=["Привилегии пользователя"])


@router.get("/posts/all")
async def get_posts_all(post_data: PostsSchemas = Depends(get_current_is_user)):
    return await PostsDAO.get_post_all()


@router.get("/posts/{post_id}")
async def get_posts(post_id, post_data: PostsSchemas = Depends(get_current_is_user)):
    post = await PostsDAO.get_post(post_id)
    if post is None:
        return {"message": "Пользователь с данным id не найден"}
    return post


@router.post("/posts")
async def add_posts(post: Annotated[PostsSchemas, Depends()],
                    post_data: PostsSchemas = Depends(get_current_is_user)):
    data_post = post.dict()
    data_post["user_id"] = post_data.id
    return await PostsDAO.add_post(data_post)


@router.put("/posts/{post_id}")
async def update_posts(post_update: PostsSchemas,
                       post_data: UsersAuthorizationSchema = Depends(get_current_is_user),
                       post: PostsSchemas = Depends(PostsDAO.get_post)):
    return await PostsDAO.update_post(post, post_update)


@router.delete("/posts/all")
async def delete_posts_all(post_data: PostsSchemas = Depends(get_current_is_user)):
    return await PostsDAO.delete_posts_all()


@router.delete("posts/{post_id}")
async def delete_posts(post_id):
    return await PostsDAO.delete_post(post_id)


@router.get("/me", name="Данные обо мне")
async def get_me(user_data: UsersAuthorizationSchema = Depends(get_current_is_user)):
    return user_data
