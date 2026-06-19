
from typing import Optional, List, TYPE_CHECKING
from datetime import date
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.library import Library

class User(SQLModel, table=True):
    __tablename__ = "tb_usuarios"

    usr_admin: bool = Field(
    default=False
    )
    
    usr_id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    usr_avatar_url: Optional[str] = Field(
    default=None,
    max_length=255
    )
    
    usr_nome_usuario: str = Field(
        unique=True,
        index=True,
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
        min_length= 8,
        max_length=255
    )

    usr_bio: Optional[str] = Field(
    default=None,
    max_length=500
    )
    
    usr_created_at: date = Field(
        default_factory=date.today
    )

    # Um usuário pode ter vários jogos na biblioteca
    biblioteca: list["Library"] = Relationship(
            back_populates="usuario"
        )
