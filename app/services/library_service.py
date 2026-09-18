from abc import ABC, abstractmethod

from app.models.library import Library
from app.schemas.library import LibraryCreate, LibraryUpdate, LibraryFilters


class LibraryService(ABC):

    @abstractmethod
    def adicionar_jogo(
        self,
        usuario_id: int,
        dados: LibraryCreate
    ) -> Library:
        pass

    @abstractmethod
    def listar_biblioteca(
        self,
        usuario_id: int,
        filtros: LibraryFilters | None = None
    ) -> list[Library]:
        pass

    @abstractmethod
    def buscar_por_id(
        self,
        usuario_id: int,
        bib_id: int
    ) -> Library:
        pass

    @abstractmethod
    def atualizar(
        self,
        usuario_id: int,
        bib_id: int,
        dados: LibraryUpdate
    ) -> Library:
        pass

    @abstractmethod
    def remover(
        self,
        usuario_id: int,
        bib_id: int
    ):
        pass