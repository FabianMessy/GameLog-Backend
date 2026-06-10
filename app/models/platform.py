from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from models.game import Game
from models.game_platform import GamePlatform

class Platform(SQLModel, table=True):
    __tablename__ = "tb_plataformas"

    plt_id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    plt_nome: str = Field(
        unique=True,
        min_length=2,
        max_length=50
    )

    jogos: List["Game"] = Relationship(
        back_populates="plataformas",
        link_model=GamePlatform
    )