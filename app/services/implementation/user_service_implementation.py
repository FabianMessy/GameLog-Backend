from fastapi import HTTPException

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.users import User
from app.repositories.users_repository import UsersRepository
from app.schemas.user import UserCreate
from app.services.user_service import UserService


class UserServiceImpl(UserService):

    def __init__(self, repository: UsersRepository):
        self.repository = repository

    def registrar(self, dados: UserCreate) -> User:
        usuario_existente = self.repository.get_by_email(dados.usr_email)

        if usuario_existente:
            raise HTTPException(
                status_code=400,
                detail="Email já cadastrado"
            )

        novo_usuario = User(
            usr_nome_usuario=dados.usr_nome_usuario,
            usr_nome_completo=dados.usr_nome_completo,
            usr_email=dados.usr_email,
            usr_senha=hash_password(dados.usr_senha),
            usr_bio=dados.usr_bio,
            usr_avatar_url=str(dados.usr_avatar_url) if dados.usr_avatar_url else None,
        )

        return self.repository.create(novo_usuario)

    def autenticar(self, email: str, senha: str) -> str:
        usuario = self.repository.get_by_email(email)

        if not usuario or not verify_password(senha, usuario.usr_senha):
            raise HTTPException(
                status_code=401,
                detail="Email ou senha inválidos"
            )

        return create_access_token(
            {
                "user_id": usuario.usr_id,
                "email": usuario.usr_email,
                "admin": usuario.usr_admin,
            }
        )

    def buscar_por_id(self, user_id: int) -> User:
        usuario = self.repository.get_by_id(user_id)

        if not usuario:
            raise HTTPException(
                status_code=404,
                detail="Usuário não encontrado"
            )

        return usuario
