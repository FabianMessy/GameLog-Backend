from pydantic import BaseModel, Field


class PlatformCreate(BaseModel):
    plt_nome: str = Field(
        min_length=2,
        max_length=50
    )

class PlatformUpdate(BaseModel):
    plt_nome: str = Field(
        min_length=2,
        max_length=50
    )

class PlatformResponse(BaseModel):
    plt_id: int
    plt_nome: str

    model_config = {
        "from_attributes": True
    }

class PlatformSimpleResponse(BaseModel):
    plt_id: int
    plt_nome: str

    model_config = {
        "from_attributes": True
    }