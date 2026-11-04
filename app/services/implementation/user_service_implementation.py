from fastapi import HTTPException

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.users import User
from app.repositories.users_repository import UsersRepository
from app.schemas.user import UserCreate, UserUpdate
from app.services.user_service import UserService


class UserServiceImpl(UserService):

    def __init__(self, repository: UsersRepository):
        self.repository = repository

    def registrar(self, dados: UserCreate) -> User:
        if self.repository.get_by_email(dados.usr_email):
            raise HTTPException(
                status_code=400,
                detail="Email já cadastrado"
            )

        if self.repository.get_by_username(dados.usr_nome_usuario):
            raise HTTPException(
                status_code=400,
                detail="Nome de usuário já está em uso"
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

    def atualizar(self, user_id: int, dados: UserUpdate) -> User:
        usuario = self.buscar_por_id(user_id)

        # exclude_unset: só o que o cliente realmente enviou. Isso permite
        # distinguir "não mexe" (campo ausente) de "limpa" (avatar/bio = null).
        campos = dados.model_dump(exclude_unset=True)

        # Reenviar o próprio valor não é conflito; só barra se pertence a OUTRA pessoa.
        novo_email = campos.get("usr_email")
        if novo_email is not None and novo_email != usuario.usr_email:
            dono = self.repository.get_by_email(novo_email)
            if dono and dono.usr_id != usuario.usr_id:
                raise HTTPException(
                    status_code=400,
                    detail="Email já cadastrado"
                )

        novo_nome = campos.get("usr_nome_usuario")
        if novo_nome is not None and novo_nome != usuario.usr_nome_usuario:
            dono = self.repository.get_by_username(novo_nome)
            if dono and dono.usr_id != usuario.usr_id:
                raise HTTPException(
                    status_code=400,
                    detail="Nome de usuário já está em uso"
                )

        # O schema devolve HttpUrl; a coluna é string.
        if campos.get("usr_avatar_url") is not None:
            campos["usr_avatar_url"] = str(campos["usr_avatar_url"])

        for campo, valor in campos.items():
            setattr(usuario, campo, valor)

        return self.repository.update(usuario)