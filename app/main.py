from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import create_db

from app.routes.auth import router as auth_router
from app.routes.games import router as games_router
import app.models

from app.core.cors import configure_cors

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    yield

app = FastAPI(lifespan=lifespan)

configure_cors(app)

app.include_router(auth_router)
app.include_router(games_router)
