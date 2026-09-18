from __future__ import annotations
from datetime import date, datetime
from pydantic import BaseModel

from app.models.library import LibraryStatus

from app.schemas.user import UserSimpleResponse
from app.schemas.game import GameSimpleResponse



class LibraryFilters(BaseModel):
    avaliacao_min: int | None = None
    avaliacao_max: int | None = None

    lancamento_inicio: date | None = None
    lancamento_fim: date | None = None

    generos: list[str] | None = None
    status: list[LibraryStatus] | None = None

    horas_min: int | None = None
    horas_max: int | None = None

    classificacoes: list[str] | None = None

class LibraryCreate(BaseModel):
    bib_status: LibraryStatus
    bib_jgs_id: int
    bib_usr_nota: int | None = None
    bib_usr_avaliacao: str | None = None
    bib_jgs_favorito: bool = False
    bib_jgs_horas_jogadas: int = 0


class LibraryUpdate(BaseModel):
    bib_status: LibraryStatus | None = None

    bib_usr_nota: int | None = None
    bib_usr_avaliacao: str | None = None

    bib_jgs_favorito: bool | None = None
    bib_jgs_horas_jogadas: int | None = None


class LibrarySimpleResponse(BaseModel):
    bib_id: int

    bib_status: LibraryStatus

    bib_updated_at: datetime
    bib_jgs_add_at: date

    bib_usr_nota: int | None
    bib_usr_avaliacao: str | None

    bib_jgs_favorito: bool
    bib_jgs_horas_jogadas: int

    bib_usr_id: int
    bib_jgs_id: int

    model_config = {
        "from_attributes": True
    }

class LibraryDetailResponse(LibrarySimpleResponse):
    usuario: UserSimpleResponse
    jogo: GameSimpleResponse

class LibraryReviewResponse(BaseModel):
    bib_id: int

    bib_usr_nota: int | None
    bib_usr_avaliacao: str | None

    bib_updated_at: datetime

    usuario: UserSimpleResponse

    model_config = {
        "from_attributes": True
    }

from app.schemas.user import UserSimpleResponse
from app.schemas.game import GameSimpleResponse

LibraryDetailResponse.model_rebuild()
LibraryReviewResponse.model_rebuild()
