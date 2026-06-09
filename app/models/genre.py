from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from models.game import Game
from models.game_genre import GameGenre

class Genre(SQLModel, table=True):
    __tablename__ = "tb_generos"

    gen_id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    gen_nome: str = Field(
        unique=True,
        max_length=50
    )

    jogos: List["Game"] = Relationship(
        back_populates="generos",
        link_model=GameGenre
    )