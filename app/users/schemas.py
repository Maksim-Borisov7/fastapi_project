from typing import Optional
from pydantic import BaseModel, Field, EmailStr, ConfigDict


class UsersAuthorizationSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str = Field(max_length=20, description="имя пользователя до 20 символов")
    password: str = Field(min_length=3, max_length=20, description="пароль от 3 до 20 символов")


class UsersRegistrationSchema(UsersAuthorizationSchema, BaseModel):
    email: EmailStr
    about_me: None | str = None


class UsersUpdateSchema(UsersRegistrationSchema):
    id: int
    is_super_admin: Optional[bool] = False
    is_user: Optional[bool] = False
