from pydantic import BaseModel

class GenreCreate(BaseModel):
    gen_nome: str

class GenreUpdate(BaseModel):
    gen_nome: str

class GenreResponse(BaseModel):
    gen_id: int
    gen_nome: str

    model_config = {
        "from_attributes": True
    }