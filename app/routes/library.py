from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_library_service
from app.schemas.library import (
    LibraryCreate,
    LibraryDetailResponse,
    LibrarySimpleResponse,
    LibraryUpdate
)
from app.services.library_service import LibraryService

router = APIRouter(
    prefix="/library",
    tags=["Biblioteca"]
)


from app.core.dependencies_auth import CurrentUser 

@router.post("/")
def adicionar_jogo(
    dados: LibraryCreate,
    current_user: CurrentUser,
    service: Annotated[
        LibraryService,
        Depends(get_library_service)
    ]
):
    return service.adicionar_jogo(
        current_user.usr_id,
        dados
    )


@router.get("/")
def listar_biblioteca(
    current_user: CurrentUser,
    service: Annotated[
        LibraryService,
        Depends(get_library_service)
    ]
):
    return service.listar_biblioteca(current_user.usr_id)


@router.get(
    "/{bib_id}",
    response_model=LibraryDetailResponse
)
def buscar_biblioteca(
    bib_id: int,
    service: Annotated[
        LibraryService,
        Depends(get_library_service)
    ]
):
    return service.buscar_por_id(bib_id)


@router.put(
    "/{bib_id}",
    response_model=LibraryDetailResponse
)
def atualizar_biblioteca(
    bib_id: int,
    dados: LibraryUpdate,
    service: Annotated[
        LibraryService,
        Depends(get_library_service)
    ]
):
    return service.atualizar(bib_id, dados)


@router.delete(
    "/{bib_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def remover_biblioteca(
    bib_id: int,
    service: Annotated[
        LibraryService,
        Depends(get_library_service)
    ]
):
    service.remover(bib_id)