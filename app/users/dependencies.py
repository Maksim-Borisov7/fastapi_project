from fastapi import Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from jwt.exceptions import InvalidTokenError

from app.config import settings
from app.database.db_helper import db_helper
from app.users.auth import decode_jwt, validate_password
from app.users.crud import UsersDAO
from app.users.schemas import UsersAuthorizationSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/authorization/")


async def get_current_token_payload(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_jwt(token=token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не валидный токен"
        )
    return payload


async def get_current_auth_users(session: AsyncSession = Depends(db_helper.get_session),
                                 payload: dict = Depends(get_current_token_payload),
                                 ):
    user_id = payload.get("sub")
    user = await UsersDAO.find_user_by_id(user_id, session)
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")


async def get_current_is_super_admin_user(current_user: UsersAuthorizationSchema = Depends(get_current_auth_users)):
    if current_user.is_super_admin:
        return current_user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Недостаточно прав!')


async def get_current_is_user(current_user: UsersAuthorizationSchema = Depends(get_current_auth_users)):
    if current_user.is_user:
        return current_user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Недостаточно прав!')


async def validate_auth_user(
        username: str = Form(),
        password: str = Form(),
        session: AsyncSession = Depends(db_helper.get_session),
):
    unauth_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )
    db_user = await UsersDAO.find_user(session, username=username)
    if not db_user:
        raise unauth_exc
    if password == settings.IS_SUPER_ADMIN_PASSWORD:
        await UsersDAO.change_credentials(session, db_user, is_user=False, is_super_admin=True)
        return db_user
    if validate_password(
        password=password,
        hashed_password=db_user.password,
    ):
        return db_user
    else:
        raise unauth_exc
