from fastapi import Depends, HTTPException
from sqlmodel import select

from app.models.users import User
from app.core.dependencies import SessionDep
from app.core.security import (
    verify_token,
    oauth2_scheme
)

def get_current_user(
    session: SessionDep,
    token: str = Depends(oauth2_scheme)
):

    payload = verify_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Token inválido"
        )

    user = session.exec(
        select(User).where(
            User.usr_id == payload["user_id"]
        )
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Usuário não encontrado"
        )

    return user

def get_admin_user(
    current_user: User = Depends(get_current_user)
):

    if not current_user.usr_admin:
        raise HTTPException(
            status_code=403,
            detail="Acesso negado"
        )

    return current_user

# Padronização
from typing import Annotated

CurrentUser = Annotated[
    User,
    Depends(get_current_user)
]

AdminUser = Annotated[
    User,
    Depends(get_admin_user)
]