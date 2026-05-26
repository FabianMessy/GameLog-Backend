from typing import Optional
from datetime import date
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    __tablename__ = "tb_usuarios"

    usr_id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    usr_nome_usuario: str = Field(
        max_length=80
    )

    usr_nome_completo: str = Field(
        max_length=80
    )

    usr_email: str = Field(
        unique=True,
        index=True,
        max_length=80
    )

    usr_senha: str = Field(
        max_length=45
    )

    usr_created_at: date = Field(
        default_factory=date.today
    )