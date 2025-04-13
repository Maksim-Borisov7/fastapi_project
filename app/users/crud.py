from fastapi import HTTPException
from starlette import status
from app.database.methods import session_factory, DBmethods
from sqlalchemy import select, delete, update
from app.database.models import UsersModel


class UsersDAO(DBmethods):
    model = UsersModel

    @classmethod
    async def add(cls, **values):
        async with session_factory() as session:
            user = cls.model(**values)
            session.add(user)
            await session.commit()

    @classmethod
    async def find_all(cls):
        async with session_factory() as session:
            stmt = select(cls.model)
            result = await session.execute(stmt)
            return result.scalars().all()

    @classmethod
    async def find_user(cls, username):
        async with session_factory() as session:
            query = select(cls.model).filter_by(username=username)
            res = await session.execute(query)
            return res.scalar()

    @classmethod
    async def delete_all(cls):
        async with session_factory() as session:
            await session.execute(delete(cls.model))
            await session.commit()
            return {"message": "Пользователи успешно удалены"}

    @classmethod
    async def delete_user_by_username(cls, user):
        async with session_factory() as session:
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Пользователь не найден"
                )
            await session.execute(delete(user))
            await session.commit()
            return {"msg": f"Пользователь с ником {user.username} успешно удалён"}

    @classmethod
    async def update_user(cls, user, user_update):
        async with session_factory() as session:
            if user is None:
                return {"message": "Пользователь не был найден"}
            user_dict = user_update.model_dump()
            stmt = (
                update(cls.model)
                .where(cls.model.id == user.id)
                .values(**user_dict)
                .execution_options(synchronize_session="fetch")
            )
            await session.execute(stmt)
            await session.commit()
            return {"message": "Пользователь изменён"}
