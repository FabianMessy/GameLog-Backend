from sqlmodel import create_engine, Session, SQLModel

from app.core.config import DATABASE_URL

from app.models.users import User
from app.models.game import Game
from app.models.genre import Genre
from app.models.platform import Platform
from app.models.game_genre import GameGenre
from app.models.game_platform import GamePlatform
from app.models.library import Library

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}


engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False}
)

def create_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session