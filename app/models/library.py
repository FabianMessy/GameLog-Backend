from typing import Optional, List
from datetime import date, datetime
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
from sqlalchemy import UniqueConstraint

from models.game import Game
from models.users import User

class LibraryStatus(str, Enum):
    JOGANDO = "jogando"
    COMPLETO = "completo"
    PAUSADO = "pausado"
    ABANDONADO = "abandonado"
    PLANEJADO = "planejado"
    
class Library(SQLModel, table=True):
    __tablename__ = "tb_biblioteca"

    __table_args__ = (
        UniqueConstraint(
            "bib_usr_id",
            "bib_jgs_id",
            name="uq_usuario_jogo"
        ),
    )
     
    bib_id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    bib_status: LibraryStatus = Field()

    bib_updated_at: datetime = Field(
    default_factory=datetime.now
    )

    bib_usr_nota: Optional[int] = Field(
        default=None,
        ge=0,
        le=10
    )

    bib_usr_avaliacao: Optional[str] = Field(
        default=None,
        max_length=500
    )

    bib_jgs_add_at: date = Field(
        default_factory=date.today
    )

    bib_jgs_favorito: bool = Field(
    default=False
    )

    bib_jgs_horas_jogadas: int = Field(
    default=0
    )
    
    bib_usr_id: int = Field(
        foreign_key="tb_usuarios.usr_id"
    )

    bib_jgs_id: int = Field(
        foreign_key="tb_jogos.jgs_id"
    )

    # Relacionamentos
    usuario: "User" = Relationship(
        back_populates="biblioteca"
    )

    jogo: "Game" = Relationship(
        back_populates="bibliotecas"
    )