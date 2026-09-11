

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

    # Id do jogo na RAWG, quando o registro veio de lá (import em lote
    # do admin ou "Adicionar à Biblioteca" no catálogo). Nulo pra jogo
    # cadastrado manualmente. É o que permite, por exemplo, ir de um
    # jogo salvo na biblioteca de volta pra sua página de detalhes
    # (antes disso não existia, e o dedup de import dependia só do
    # título, o que é frágil).
    jgs_rawg_id: Optional[int] = Field(
        default=None,
        unique=True,
        index=True,
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

    # Tempo médio de conclusão do jogo (em horas) — dado geral do jogo,
    # vem do campo "playtime" da RAWG. NÃO é o tempo jogado por um
    # usuário específico (isso é bib_jgs_horas_jogadas, em
    # tb_biblioteca); é o mesmo tipo de número que um HowLongToBeat
    # mostra. Usado pelo filtro "Tempo de Jogo" da Biblioteca.
    jgs_tempo_medio_horas: Optional[int] = Field(
        default=None
    )

    # Classificação indicativa aproximada, em rótulo brasileiro
    # ("Livre", "10", "12", "14", "16", "+18"). A RAWG não tem ClassInd
    # — só ESRB (americana), e nem todo jogo tem isso preenchido. Esse
    # campo é uma APROXIMAÇÃO calculada a partir do ESRB no momento da
    # importação (ver _mapear_esrb_para_classind em
    # rawg_import_service.py); nunca é a classificação oficial
    # brasileira do jogo. Fica None quando a RAWG não informa ESRB.
    jgs_classificacao_indicativa: Optional[str] = Field(
        default=None,
        max_length=10,
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