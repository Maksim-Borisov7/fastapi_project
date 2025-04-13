from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from app.users.crud import UsersDAO
from app.users.dependencies import get_current_user, get_current_is_super_admin_user
from app.database.models import UsersModel
from app.users.schemas import UsersAuthorizationSchema, UsersUpdateSchema

router = APIRouter(prefix="/admin", tags=["Привилегии админтистратора"])


@router.get("/me/", name="Данные обо мне")
async def get_me(user_data: UsersAuthorizationSchema = Depends(get_current_user)):
    return user_data


@router.get("/users/", name="Данные о всех пользователей")
async def get_all_users(user_data: UsersAuthorizationSchema = Depends(get_current_is_super_admin_user)):
    return await UsersDAO.find_all()


@router.get("/users/{username}/")
async def get_user(username, user_data: UsersAuthorizationSchema = Depends(get_current_is_super_admin_user)):
    user = await UsersDAO.find_one_or_none(username=username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Пользователь с username '{username}' не найден"
        )
    return user


@router.delete("/users/")
async def delete_all_users(user_data: UsersAuthorizationSchema = Depends(get_current_is_super_admin_user)) -> dict:
    return await UsersDAO.delete_all()


@router.delete("/users/{username}/")
async def delete_user(user_data: UsersAuthorizationSchema = Depends(get_current_is_super_admin_user),
                      user: UsersAuthorizationSchema = Depends(UsersDAO.find_user)):
    return await UsersDAO.delete_user_by_username(user)


@router.put("/users/{username}")
async def update_user(user_update: UsersUpdateSchema,
                      user_data: UsersAuthorizationSchema = Depends(get_current_is_super_admin_user),
                      user: UsersModel = Depends(UsersDAO.find_user)):
    return await UsersDAO.update_user(user, user_update)

