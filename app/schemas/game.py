from __future__ import annotations
from datetime import date
from pydantic import BaseModel, HttpUrl, field_validator

from app.services.filtro_conteudo import CLASSIFICACAO_PADRAO
from app.schemas.genre import GenreSimpleResponse
from app.schemas.platform import PlatformSimpleResponse

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
    jgs_rawg_id: int | None = None
    jgs_titulo: str
    jgs_descricao: str
    jgs_lancamento: date
    jgs_desenvolvedor: str
    jgs_distribuidor: str
    jgs_capa_url: HttpUrl | None
    jgs_nota_media: float
    jgs_tempo_medio_horas: int | None = None
    jgs_classificacao_indicativa: str = CLASSIFICACAO_PADRAO

    model_config = {
        "from_attributes": True
    }

    @field_validator("jgs_classificacao_indicativa", mode="before")
    @classmethod
    def _sem_classificacao_vira_padrao(cls, valor):
        # Jogos salvos antes desta regra ainda têm NULL no banco.
        return valor or CLASSIFICACAO_PADRAO

class GameDetailResponse(GameSimpleResponse):
    generos: list[GenreSimpleResponse]
    plataformas: list[PlatformSimpleResponse]