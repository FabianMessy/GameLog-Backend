from __future__ import annotations
from datetime import date
from pydantic import BaseModel, EmailStr, Field, HttpUrl, field_validator

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.schemas.library import LibrarySimpleResponse

class UserCreate(BaseModel):
    usr_nome_usuario: str = Field(min_length=3, max_length=80)
    usr_nome_completo: str = Field(min_length=1, max_length=80)
    usr_email: EmailStr
    # 8 a 72: o bcrypt só considera os primeiros 72 bytes da senha.
    usr_senha: str = Field(min_length=8, max_length=72)

    usr_avatar_url: HttpUrl | None = None
    usr_bio: str | None = None

class UserLogin(BaseModel):
    usr_email: EmailStr
    usr_senha: str

class UserUpdate(BaseModel):
    """
    Corpo do PATCH /auth/me. Todos os campos são opcionais: só o que for
    enviado é alterado (o service usa model_dump(exclude_unset=True)).

    - nome de usuário, nome completo e e-mail são obrigatórios no banco,
      então enviar null (ou texto em branco) neles é rejeitado.
    - avatar e bio podem ser null/"" pra limpar o campo.
    - usr_admin e senha não existem aqui de propósito: o Pydantic ignora
      campos extras, então ninguém consegue se promover a admin por essa rota.
    """
    usr_nome_usuario: str | None = Field(default=None, max_length=80)
    usr_nome_completo: str | None = Field(default=None, max_length=80)
    usr_email: EmailStr | None = None

    usr_avatar_url: HttpUrl | None = None
    usr_bio: str | None = Field(default=None, max_length=500)

    @field_validator("usr_nome_usuario", "usr_nome_completo")
    @classmethod
    def _texto_obrigatorio(cls, valor: str | None):
        # Campo omitido não passa por aqui; só chega None se vier null explícito.
        if valor is None:
            raise ValueError("não pode ser nulo")
        valor = valor.strip()
        if not valor:
            raise ValueError("não pode ficar em branco")
        return valor

    @field_validator("usr_email")
    @classmethod
    def _email_obrigatorio(cls, valor):
        if valor is None:
            raise ValueError("não pode ser nulo")
        return valor

    @field_validator("usr_avatar_url")
    @classmethod
    def _avatar_cabe_no_banco(cls, valor):
        # usr_avatar_url é VARCHAR(255) no banco
        if valor is not None and len(str(valor)) > 255:
            raise ValueError("a URL do avatar deve ter no máximo 255 caracteres")
        return valor

    @field_validator("usr_bio")
    @classmethod
    def _bio_vazia_vira_nula(cls, valor: str | None):
        if valor is None:
            return None
        valor = valor.strip()
        return valor or None


class UserPasswordChange(BaseModel):
    """
    Corpo do PATCH /auth/me/senha. A senha atual é exigida para que quem
    pegar uma sessão aberta não consiga trocar a senha da conta.
    """
    usr_senha_atual: str = Field(min_length=1, max_length=72)
    # 8 a 72: mesmas regras do cadastro (o bcrypt só olha os 72 primeiros bytes).
    usr_senha_nova: str = Field(min_length=8, max_length=72)

    @field_validator("usr_senha_nova")
    @classmethod
    def _senha_com_numero(cls, valor: str):
        # Regra do protótipo: mínimo de 8 caracteres e pelo menos 1 número.
        if not any(c.isdigit() for c in valor):
            raise ValueError("a senha deve ter pelo menos 1 número")
        return valor


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

# Só o que pode ser mostrado pra qualquer visitante (ex.: reviews públicas).
# Nunca incluir e-mail nem nome completo aqui.
class UserPublicResponse(BaseModel):
    usr_id: int

    usr_nome_usuario: str
    usr_avatar_url: HttpUrl | None

    model_config = {
        "from_attributes": True
    }

class UserDetailResponse(UserSimpleResponse):
    biblioteca: list[LibrarySimpleResponse]

from app.schemas.library import LibrarySimpleResponse

UserDetailResponse.model_rebuild()