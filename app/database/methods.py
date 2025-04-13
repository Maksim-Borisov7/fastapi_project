from sqlalchemy import select
from app.core.config import PG_URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.database.models import Base

engine = create_async_engine(PG_URL)

session_factory = async_sessionmaker(engine, expire_on_commit=False)


class DBmethods:
    model = None

    @staticmethod
    async def create_table():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def delete_table():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with session_factory() as session:
            query = select(cls.model).filter_by(**filter_by)
            res = await session.execute(query)
            return res.scalar_one_or_none()

    @classmethod
    async def find_one_or_none_by_id(cls, data_id: int):
        async with session_factory() as session:
            query = select(cls.model).filter_by(id=int(data_id))
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def change_credentials(cls, username, is_user=bool, is_super_admin=bool):
        async with session_factory() as session:
            user = await cls.find_one_or_none(username=username)
            if user is None:
                return None
            user.is_user = is_user
            user.is_super_admin = is_super_admin
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

