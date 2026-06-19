
from typing import Optional
from sqlmodel import SQLModel, Field

class GamePlatform(SQLModel, table=True):
    __tablename__ = "tb_jogos_plataformas"

    jgs_id: int = Field(
        foreign_key="tb_jogos.jgs_id",
        primary_key=True
    )

    plt_id: int = Field(
        foreign_key="tb_plataformas.plt_id",
        primary_key=True
    )