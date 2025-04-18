from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from app.database.db_helper import db_helper
from app.users.auth import encode_jwt, hash_password
from app.users.crud import UsersDAO
from app.users.dependencies import validate_auth_user
from app.users.schemas import UsersRegistrationSchema, UsersAuthorizationSchema, TokenInfo

router = APIRouter(prefix="/auth", tags=["Регистрация и аутентификация пользователей"])


@router.post("/registration/", name="Регистрация пользователя")
async def registration(credentials: Annotated[UsersRegistrationSchema, Depends()],
                       session: AsyncSession = Depends(db_helper.get_session)) -> dict:
    logging.info("Регистрация пользователя")
    user = await UsersDAO.find_user(session, username=credentials.username)
    if user:
        return {"message": "Пользователь уже существует"}
    user_dict = credentials.dict()
    user_dict['password'] = hash_password(credentials.password)
    await UsersDAO.add_user(session, **user_dict)
    return {'message': f'Вы успешно зарегистрированы!'}


@router.post("/authorization/", name="Авторизация пользователя", response_model=TokenInfo)
async def auth_user(user: UsersAuthorizationSchema = Depends(validate_auth_user),
                    session: AsyncSession = Depends(db_helper.get_session),
                    ) -> TokenInfo:
    logging.info("Авторизация пользователя")
    jwt_payload = {
        "sub": str(user.id),
        "username": user.username,
    }
    token = encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer",
    )

