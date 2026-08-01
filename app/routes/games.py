from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.schemas.game import (
    GameCreate,
    GameDetailResponse,
    GameSimpleResponse,
    GameUpdate,
)

from app.core.dependencies import SessionDep
from app.core.dependencies_auth import AdminUser
from app.core.dependencies_game import get_game_service

from app.services.rawg_service import buscar_jogos_rawg
from app.services.rawg_import_service import importar_jogos_rawg
from app.services.game_service import GameService

router = APIRouter(prefix="/games", tags=["Games"])


@router.post("/")
def criar_jogo(
    dados: GameCreate,
    user: AdminUser,
    service: Annotated[GameService, Depends(get_game_service)],
):
    jogo = service.criar_jogo(dados)
    return {
        "message": f"Jogo (id:{jogo.jgs_id}) cadastrado com sucesso!",
        "id": jogo.jgs_id,
    }


@router.get("/", response_model=list[GameSimpleResponse])
def listar_jogos(
    service: Annotated[GameService, Depends(get_game_service)],
):
    return service.listar_jogos()


@router.get("/rawg/search")
def buscar_na_rawg(
    nome: str,
    page_size: int = 10,
    page: int = 1,
):
    try:
        return buscar_jogos_rawg(
            nome=nome,
            page_size=page_size,
            page=page,
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/rawg/importar")
def importar_rawg_para_banco(
    session: SessionDep,
    user: AdminUser,
    search: str | None = None,
    pages: int = 1,
    page_size: int = 10,
):
    try:
        return importar_jogos_rawg(
            session=session,
            search=search,
            pages=pages,
            page_size=page_size,
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/{game_id}", response_model=GameDetailResponse)
def get_game_by_id(
    game_id: int,
    service: Annotated[GameService, Depends(get_game_service)],
):
    return service.buscar_por_id(game_id)


@router.put("/{game_id}", response_model=GameDetailResponse)
def atualizar_jogo(
    game_id: int,
    dados: GameUpdate,
    user: AdminUser,
    service: Annotated[GameService, Depends(get_game_service)],
):
    return service.atualizar(game_id, dados)


@router.delete("/{game_id}", status_code=204)
def remover_jogo(
    game_id: int,
    user: AdminUser,
    service: Annotated[GameService, Depends(get_game_service)],
):
    service.remover(game_id)
