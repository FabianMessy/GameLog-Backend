from typing import Optional
from datetime import date

from sqlmodel import SQLModel, Field


class Game(SQLModel, table=True):
    __tablename__ = "tb_jogos"

    jgs_id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    jgs_titulo: str = Field(
        max_length=45
    )

    jgs_descricao: str = Field(
        max_length=120
    )

    jgs_lancamento: date

    jgs_desenvolvedor: str = Field(
        max_length=120
    )

    jgs_distribuidor: str = Field(
        max_length=120
    )

    jgs_nota_media: int = Field(
        default=0
    )