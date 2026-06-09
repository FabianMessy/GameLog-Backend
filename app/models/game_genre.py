from typing import Optional
from sqlmodel import SQLModel, Field

class GameGenre(SQLModel, table=True):
    __tablename__ = "tb_jogos_generos"

    jgs_id: int = Field(
        foreign_key="tb_jogos.jgs_id",
        primary_key=True
    )

    gen_id: int = Field(
        foreign_key="tb_generos.gen_id",
        primary_key=True
    )