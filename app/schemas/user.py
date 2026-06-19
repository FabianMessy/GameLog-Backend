from __future__ import annotations
from datetime import date
from pydantic import BaseModel, EmailStr, HttpUrl

from typing import TYPE_CHECKING    
if TYPE_CHECKING:
    from app.schemas.library import LibrarySimpleResponse

class UserCreate(BaseModel):
    usr_nome_usuario: str
    usr_nome_completo: str
    usr_email: EmailStr
    usr_senha: str

    usr_avatar_url: HttpUrl | None = None
    usr_bio: str | None = None

class UserLogin(BaseModel):
    usr_email: EmailStr
    usr_senha: str

class UserUpdate(BaseModel):
    usr_nome_usuario: str | None = None
    usr_nome_completo: str | None = None
    usr_email: EmailStr | None = None

    usr_avatar_url: HttpUrl | None = None
    usr_bio: str | None = None


class UserSimpleResponse(BaseModel):
    usr_id: int

    usr_nome_usuario: str
    usr_nome_completo: str
    usr_email: EmailStr

    usr_avatar_url: HttpUrl | None
    usr_bio: str | None

    usr_created_at: date

    model_config = {
        "from_attributes": True
    }

class UserDetailResponse(UserSimpleResponse):
    biblioteca: list[LibrarySimpleResponse]