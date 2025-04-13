from typing import Annotated
from fastapi import APIRouter, Depends
from starlette.responses import Response
import logging
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.crud import UsersDAO
from app.users.schemas import UsersRegistrationSchema, UsersAuthorizationSchema
from app.core.config import ACCESS_TOKEN_COOKIE_NAME

router = APIRouter(prefix="/auth", tags=["Регистрация и аутентификация пользователей"])


@router.post("/registration", name="Регистрация пользователя")
async def registration(credentials: Annotated[UsersRegistrationSchema, Depends()]) -> dict:
    logging.info("Регистрация пользователя")
    user = await UsersDAO.find_one_or_none(username=credentials.username)
    if user:
        return {"message": "Пользователь уже существует"}
    user_dict = credentials.dict()
    user_dict['password'] = get_password_hash(credentials.password)
    await UsersDAO.add(**user_dict)
    return {'message': f'Вы успешно зарегистрированы!'}


@router.post("/authorization", name="Авторизация пользователя")
async def auth_user(response: Response, user: Annotated[UsersAuthorizationSchema, Depends()]) -> dict:
    logging.info("Авторизация пользователя")
    check = await authenticate_user(user)
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key=ACCESS_TOKEN_COOKIE_NAME, value=access_token, httponly=True)
    # await DBmethods.change_credentials(check)
    return {'access_token': access_token, "refresh_token": None}


@router.post("/logout/", name="Выход пользователя из системы")
async def logout_user(response: Response):
    logging.info("Выход пользователя из системы")
    response.delete_cookie(key=ACCESS_TOKEN_COOKIE_NAME)
    return {'message': 'Пользователь успешно вышел из системы'}