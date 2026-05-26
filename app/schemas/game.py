from datetime import date
from pydantic import BaseModel


class GameCreate(BaseModel):
    jgs_titulo: str
    jgs_descricao: str
    jgs_lancamento: date
    jgs_desenvolvedor: str
    jgs_distribuidor: str


class GameResponse(BaseModel):
    jgs_id: int
    jgs_titulo: str
    jgs_descricao: str
    jgs_lancamento: date
    jgs_desenvolvedor: str
    jgs_distribuidor: str
    jgs_nota_media: int