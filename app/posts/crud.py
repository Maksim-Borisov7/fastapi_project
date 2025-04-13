import logging
from sqlalchemy import select, delete, update
from app.database.methods import session_factory, DBmethods
from app.database.models import PostsModels


class PostsDAO(DBmethods):
    model = PostsModels

    @classmethod
    async def add_post(cls, data_posts):
        logging.info("Добавить пост")
        async with session_factory() as session:
            post = cls.model(**data_posts)
            session.add(post)
            await session.commit()
            return {"message": "Пост успешно добавлен"}

    @staticmethod
    async def get_post_all():
        logging.info("Посмотреть все посты")
        async with session_factory() as session:
            query = select(PostsModels)
            result = await session.execute(query)
            return result.scalars().all()

    @staticmethod
    async def get_post(post_id: int):
        logging.info("Посмотреть пост по id")
        async with session_factory() as session:
            query = select(PostsModels).filter(PostsModels.id == int(post_id))
            result = await session.execute(query)
            return result.scalar()

    @classmethod
    async def delete_posts_all(cls):
        logging.info("Удалить все посты")
        async with session_factory() as session:
            await session.execute(delete(cls.model))
            await session.commit()
            return {"message": "Посты успешно удалены"}

    @classmethod
    async def delete_post(cls, post_id: int):
        logging.info("Удалить пост по id")
        async with session_factory() as session:
            post = await cls.find_one_or_none_by_id(post_id)
            if post is None:
                return {"message": "Пост не был найден"}
            await session.execute(delete(PostsModels).filter(PostsModels.id == int(post_id)))
            await session.commit()
            return {"message": "Пост успешно удален по id"}

    @classmethod
    async def update_post(cls, post, post_update):
        logging.info("Обновление данных в посте")
        async with session_factory() as session:
            if post is None:
                return {"message": "Пост не был найден"}
            post_dict = post_update.model_dump()
            stmt = (
                update(cls.model)
                .where(cls.model.id == post.id)
                .values(**post_dict)
                .execution_options(synchronize_session="fetch")
            )
            await session.execute(stmt)
            await session.commit()
            return {"message": "Пост изменён"}
