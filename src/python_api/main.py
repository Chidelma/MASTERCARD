from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from python_api.db.database import engine
from python_api.db.schemas import Base
from python_api.routes.users import router as users_router
from python_api.routes.tasks import router as tasks_router


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator:
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(users_router)
app.include_router(tasks_router)
