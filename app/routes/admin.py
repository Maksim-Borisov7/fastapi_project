from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.database.db_helper import db_helper
from app.users.auth import hash_password
from app.users.crud import UsersDAO
from app.users.dependencies import get_current_is_super_admin_user
from app.users.schemas import UsersAuthorizationSchema, UsersUpdateSchema

router = APIRouter(prefix="/admin", tags=["Привилегии админтистратора"])


@router.get("/me/", name="Данные обо мне")
async def get_me(user_data: UsersAuthorizationSchema = Depends(get_current_is_super_admin_user)):
    return user_data


@router.get("/users/", name="Данные о всех пользователей")
async def get_all_users(session: AsyncSession = Depends(db_helper.get_session),
                        user_data: UsersAuthorizationSchema = Depends(get_current_is_super_admin_user)):
    return await UsersDAO.find_all(session)


@router.get("/users/{username}/")
async def get_user(username,
                   session: AsyncSession = Depends(db_helper.get_session),
                   user_data: UsersAuthorizationSchema = Depends(get_current_is_super_admin_user)):
    user = await UsersDAO.find_user(session, username=username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Пользователь с username '{username}' не найден"
        )
    return user


@router.delete("/users/")
async def delete_all_users(session: AsyncSession = Depends(db_helper.get_session),
                           user_data: UsersAuthorizationSchema = Depends(get_current_is_super_admin_user)) -> dict:
    return await UsersDAO.delete_all(session)


@router.delete("/users/{username}/")
async def delete_user(username,
                      user_data: UsersAuthorizationSchema = Depends(get_current_is_super_admin_user),
                      session: AsyncSession = Depends(db_helper.get_session)):
    user = await UsersDAO.find_user(session, username=username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Пользователь с username '{username}' не найден"
        )
    return await UsersDAO.delete_user_by_username(username, session)


@router.put("/users/{username}/")
async def update_user(username,
                      user_update: UsersUpdateSchema,
                      user_data: UsersAuthorizationSchema = Depends(get_current_is_super_admin_user),
                      session: AsyncSession = Depends(db_helper.get_session)):
    user = await UsersDAO.find_user(session, username=username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Пользователь с username '{username}' не найден"
        )
    user_dict = user_update.dict()
    user_dict['password'] = hash_password(user_update.password)
    return await UsersDAO.update_user(user, user_dict, session)

