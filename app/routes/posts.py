from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from app.database.db_helper import db_helper
from app.database.models import UsersModel
from app.posts.crud import PostsDAO
from app.users.dependencies import get_current_is_user
from app.users.schemas import UsersAuthorizationSchema
from app.posts.schemas import PostsSchemas


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/authorization")
router = APIRouter(prefix="/users", tags=["Привилегии пользователя"])


@router.get("/posts/all")
async def get_my_posts_all(session: AsyncSession = Depends(db_helper.get_session),
                           post_data: PostsSchemas = Depends(get_current_is_user)):
    return await PostsDAO.get_post_all(session, post_data.id)


@router.get("/posts/{post_id}")
async def get_posts(post_id, session: AsyncSession = Depends(db_helper.get_session),
                    post_data: PostsSchemas = Depends(get_current_is_user)):
    post = await PostsDAO.get_post(post_id, session)
    if post is None:
        return {"message": "Пользователь с данным id не найден"}
    return post


@router.post("/posts")
async def add_posts(post: Annotated[PostsSchemas, Depends()],
                    session: AsyncSession = Depends(db_helper.get_session),
                    current_user: UsersAuthorizationSchema = Depends(get_current_is_user)):
    post_dict = post.model_dump()
    post_dict["user_id"] = current_user.id
    return await PostsDAO.add_post(post_dict, session)


@router.put("/posts/{post_id}")
async def update_posts(post_id,
                       post_update: PostsSchemas,
                       session: AsyncSession = Depends(db_helper.get_session),
                       post_data: UsersAuthorizationSchema = Depends(get_current_is_user),):
    post = await PostsDAO.get_post(post_id, session)
    if post is None:
        return {"message": "Пользователь с данным id не найден"}
    return await PostsDAO.update_post(post, post_update, session)


@router.delete("/posts/all")
async def delete_posts_all(session: AsyncSession = Depends(db_helper.get_session),
                           post_data: PostsSchemas = Depends(get_current_is_user)):
    return await PostsDAO.delete_posts_all(session)


@router.delete("/posts/{post_id}")
async def delete_posts(post_id, session: AsyncSession = Depends(db_helper.get_session),
                       post_data: PostsSchemas = Depends(get_current_is_user)):
    return await PostsDAO.delete_post(post_id, session)


@router.get("/me", name="Данные обо мне")
async def get_me(user_data: UsersAuthorizationSchema = Depends(get_current_is_user)):
    return user_data
