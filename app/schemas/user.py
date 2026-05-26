from datetime import date
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    usr_nome_usuario: str
    usr_nome_completo: str
    usr_email: EmailStr
    usr_senha: str


class UserLogin(BaseModel):
    usr_email: EmailStr
    usr_senha: str


class UserResponse(BaseModel):
    usr_id: int
    usr_nome_usuario: str
    usr_nome_completo: str
    usr_email: str
    usr_created_at: date