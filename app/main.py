from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.logging import setup_logging
from app.db.session import init_db, close_db
from app.api.routes import users, health

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    close_db()


app = FastAPI(title="Users API", version="1.0.0", lifespan=lifespan)

app.include_router(users.router)
app.include_router(health.router)
