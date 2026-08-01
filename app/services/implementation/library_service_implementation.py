from datetime import datetime

from fastapi import HTTPException

from app.models.library import Library
from app.repositories.library_repository import LibraryRepository
from app.schemas.library import LibraryCreate, LibraryUpdate
from app.services.library_service import LibraryService


class LibraryServiceImpl(LibraryService):

    def __init__(self, repository: LibraryRepository):
        self.repository = repository

    def adicionar_jogo(
        self,
        usuario_id: int,
        dados: LibraryCreate
    ):

        biblioteca = self.repository.get_by_user_and_game(
            usuario_id,
            dados.bib_jgs_id
        )

        if biblioteca:
            raise HTTPException(
                status_code=409,
                detail="Jogo já está na biblioteca."
            )

        novo = Library(
            **dados.model_dump(),
            bib_usr_id=usuario_id
        )

        return self.repository.create(novo)

    def listar_biblioteca(
        self,
        usuario_id: int
    ):

        return self.repository.get_by_user(usuario_id)

    def buscar_por_id(
        self,
        bib_id: int
    ):

        biblioteca = self.repository.get_by_id(bib_id)

        if not biblioteca:
            raise HTTPException(
                status_code=404,
                detail="Registro não encontrado."
            )

        return biblioteca

    def atualizar(
        self,
        bib_id: int,
        dados: LibraryUpdate
    ):

        biblioteca = self.buscar_por_id(bib_id)

        update = dados.model_dump(exclude_unset=True)

        for campo, valor in update.items():
            setattr(biblioteca, campo, valor)

        biblioteca.bib_updated_at = datetime.now()

        return self.repository.update(biblioteca)

    def remover(
        self,
        bib_id: int
    ):

        biblioteca = self.buscar_por_id(bib_id)

        self.repository.delete(biblioteca)