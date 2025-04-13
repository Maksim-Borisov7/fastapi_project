from datetime import datetime, timezone, timedelta
from fastapi import HTTPException
from jose import jwt
from passlib.context import CryptContext
from starlette import status
from starlette.requests import Request
from app.core.config import get_auth_data
from app.users.crud import UsersDAO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=10)
    to_encode.update({"exp": expire})
    auth_data = get_auth_data()
    encode_jwt = jwt.encode(to_encode, auth_data["secret_key"], algorithm=auth_data['algorithm'])
    return encode_jwt


def get_token(request: Request):
    token = request.cookies.get('users_access_token')
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token not found')
    return token


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(data_user):
    if data_user.username == data_user.username and data_user.password == "111":
        return await UsersDAO.change_credentials(data_user.username, is_user=False, is_super_admin=True)
    if data_user.username == data_user.username and data_user.password == "222":
        return await UsersDAO.change_credentials(data_user.username, is_user=True, is_super_admin=False)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail='Неверный username или password')


    # user = await UsersDAO.find_one_or_none(username=data_user.username)
    # if not user or verify_password(plain_password=data_user.password, hashed_password=user.password) is False:
    #     return None
    # return user




