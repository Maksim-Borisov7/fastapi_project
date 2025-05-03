import logging
from sqlalchemy import select, delete, update
from app.database.models import PostsModels


class PostsDAO:
    model = PostsModels

    @classmethod
    async def add_post(cls, data_posts, session):
        logging.info("Добавить пост")
        post = cls.model(**data_posts)
        session.add(post)
        await session.commit()
        return {"message": "Пост успешно добавлен"}

    @classmethod
    async def get_post_all(cls, session, user_id):
        logging.info("Посмотреть все посты")
        query = select(cls.model).where(cls.model.user_id == user_id)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def get_post(cls, post_id: int, session):
        logging.info("Посмотреть пост по id")
        query = select(PostsModels).filter(cls.model.post_id == int(post_id))
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def delete_posts_all(cls, session):
        logging.info("Удалить все посты")
        await session.execute(delete(cls.model))
        await session.commit()
        return {"message": "Посты успешно удалены"}

    @classmethod
    async def delete_post(cls, post_id: int, session):
        logging.info("Удалить пост по id")
        await session.execute(delete(PostsModels).filter(cls.model.post_id == int(post_id)))
        await session.commit()
        return {"message": "Пост успешно удален по id"}

    @classmethod
    async def update_post(cls, post, post_update, session):
        logging.info("Обновление данных в посте")
        post_dict = post_update.model_dump()
        stmt = (
            update(cls.model)
            .where(cls.model.post_id == post.post_id)
            .values(**post_dict)
            .execution_options(synchronize_session="fetch")
        )
        await session.execute(stmt)
        await session.commit()
        return {"message": "Пост изменён"}
