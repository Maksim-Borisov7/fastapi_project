from sqlalchemy import select, delete, update
from app.database.models import UsersModel


class UsersDAO:
    model = UsersModel

    @classmethod
    async def add_user(cls, session, **values):
        user = cls.model(**values)
        session.add(user)
        await session.commit()

    @classmethod
    async def find_all(cls, session):
        stmt = select(cls.model)
        result = await session.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def find_user(cls, session, username) -> UsersModel | None:
        query = select(cls.model).where(cls.model.username == username)
        res = await session.execute(query)
        return res.scalar_one_or_none()

    @classmethod
    async def find_user_by_id(cls, user_id, session):
        query = select(cls.model).filter_by(id=int(user_id))
        res = await session.execute(query)
        return res.scalar_one_or_none()

    @classmethod
    async def delete_all(cls, session):
        await session.execute(delete(cls.model))
        await session.commit()
        return {"message": "Пользователи успешно удалены"}

    @classmethod
    async def delete_user_by_username(cls, username, session):
        await session.execute(delete(cls.model).where(cls.model.username == username))
        await session.commit()
        return {"msg": f"Пользователь с ником {username} успешно удалён"}

    @classmethod
    async def update_user(cls, user, user_update, session):
        stmt = (
            update(cls.model)
            .where(cls.model.id == user.id)
            .values(**user_update)
            .execution_options(synchronize_session="fetch")
        )
        await session.execute(stmt)
        await session.commit()
        return {"message": "Пользователь изменён"}

    @classmethod
    async def change_credentials(cls, session,
                                 user, is_user=bool,
                                 is_super_admin=bool
                                 ) -> UsersModel | None:
        user.is_user = is_user
        user.is_super_admin = is_super_admin
        session.add(user)
        await session.commit()
        return user
