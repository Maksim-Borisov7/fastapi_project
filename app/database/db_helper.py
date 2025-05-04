from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from app.config import settings
from app.database.models import Base


class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(url=url, echo=echo)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def get_session(self) -> AsyncSession:
        async with self.session_factory() as session:
            yield session

    async def create_table(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def delete_table(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


db_helper = DatabaseHelper(
    url=settings.PG_URL,
    echo=settings.echo
)
