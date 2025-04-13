from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging
from app.database.methods import DBmethods
from app.routes.auth import router as router_auth
from app.routes.admin import router as router_admin
from app.routes.posts import router as router_posts

logger = logging.getLogger()
logger.setLevel(logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Запуск сервера")
    await DBmethods.delete_table()
    await DBmethods.create_table()
    logging.info("База готова к работе")
    yield
    logging.info("Выключение")


app = FastAPI(lifespan=lifespan)
app.include_router(router_auth)
app.include_router(router_posts)
app.include_router(router_admin)







