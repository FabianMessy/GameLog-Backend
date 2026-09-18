from typing import Annotated
from datetime import date

from fastapi import APIRouter, Depends, status, Query

from app.core.dependencies import get_library_service
from app.schemas.library import (
    LibraryCreate,
    LibraryDetailResponse,
    LibrarySimpleResponse,
    LibraryUpdate,
    LibraryFilters
)
from app.services.library_service import LibraryService

router = APIRouter(
    prefix="/library",
    tags=["Biblioteca"]
)


from app.core.dependencies_auth import CurrentUser 

@router.post("/", response_model=LibraryDetailResponse)
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


@router.get("/", response_model=list[LibraryDetailResponse])
def listar_biblioteca(
    current_user: CurrentUser,
    service: Annotated[
        LibraryService,
        Depends(get_library_service)
    ],
    avaliacao_min: int | None = None,
    avaliacao_max: int | None = None,
    lancamento_inicio: date | None = None,
    lancamento_fim: date | None = None,
    generos: list[str] | None = Query(default=None),
    status: list[str] | None = Query(default=None),
    horas_min: int | None = None,
    horas_max: int | None = None,
    classificacoes: list[str] | None = Query(default=None)
):
    filtros = LibraryFilters(
        avaliacao_min=avaliacao_min,
        avaliacao_max=avaliacao_max,
        lancamento_inicio=lancamento_inicio,
        lancamento_fim=lancamento_fim,
        generos=generos,
        status=status,
        horas_min=horas_min,
        horas_max=horas_max,
        classificacoes=classificacoes
    )

    return service.listar_biblioteca(current_user.usr_id, filtros)


@router.get(
    "/{bib_id}",
    response_model=LibraryDetailResponse
)
def buscar_biblioteca(
    bib_id: int,
    current_user: CurrentUser,
    service: Annotated[
        LibraryService,
        Depends(get_library_service)
    ]
):
    return service.buscar_por_id(current_user.usr_id, bib_id)


@router.put(
    "/{bib_id}",
    response_model=LibraryDetailResponse
)
def atualizar_biblioteca(
    bib_id: int,
    dados: LibraryUpdate,
    current_user: CurrentUser,
    service: Annotated[
        LibraryService,
        Depends(get_library_service)
    ]
):
    return service.atualizar(current_user.usr_id, bib_id, dados)


@router.delete(
    "/{bib_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def remover_biblioteca(
    bib_id: int,
    current_user: CurrentUser,
    service: Annotated[
        LibraryService,
        Depends(get_library_service)
    ]
):
    service.remover(current_user.usr_id, bib_id)