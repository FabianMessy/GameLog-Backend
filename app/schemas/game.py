from datetime import date
from pydantic import BaseModel, HttpUrl
from schemas.genre import GenreSimpleResponse
from schemas.platform import PlatformSimpleResponse

class GameCreate(BaseModel):
    jgs_titulo: str
    jgs_descricao: str
    jgs_lancamento: date
    jgs_desenvolvedor: str
    jgs_distribuidor: str
    jgs_capa_url: HttpUrl | None = None


class GameUpdate(BaseModel):
    jgs_titulo: str | None = None
    jgs_descricao: str | None = None
    jgs_lancamento: date | None = None
    jgs_desenvolvedor: str | None = None
    jgs_distribuidor: str | None = None
    jgs_capa_url: HttpUrl | None = None


class GameSimpleResponse(BaseModel):
    jgs_id: int
    jgs_titulo: str
    jgs_descricao: str
    jgs_lancamento: date
    jgs_desenvolvedor: str
    jgs_distribuidor: str
    jgs_capa_url: HttpUrl | None
    jgs_nota_media: float

    model_config = {
        "from_attributes": True
    }

class GameDetailResponse(GameSimpleResponse):
    generos: list[GenreSimpleResponse]
    plataformas: list[PlatformSimpleResponse]