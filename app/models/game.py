

from typing import Optional, List, TYPE_CHECKING
from datetime import date
from sqlmodel import SQLModel, Field, Relationship

from app.models.game_genre import GameGenre
from app.models.game_platform import GamePlatform

if TYPE_CHECKING:
    from app.models.library import Library
    from app.models.genre import Genre
    from app.models.platform import Platform
    
class Game(SQLModel, table=True):
    __tablename__ = "tb_jogos"

    jgs_id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    jgs_capa_url: Optional[str] = Field(
    default=None,
    max_length=255
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

    jgs_nota_media: float = Field(
        default=0.0
    )

    # Relacionamentos
    bibliotecas: List["Library"] = Relationship(
        back_populates="jogo"
    )

    generos: List["Genre"] = Relationship(
        back_populates="jogos",
        link_model=GameGenre
    )

    plataformas: List["Platform"] = Relationship(
        back_populates="jogos",
        link_model=GamePlatform
    )