from datetime import date, datetime
from pydantic import BaseModel

from models.library import LibraryStatus
from schemas.user import UserSimpleResponse
from schemas.game import GameSimpleResponse

class LibraryCreate(BaseModel):
    bib_status: LibraryStatus
    bib_usr_id: int
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