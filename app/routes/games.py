from fastapi import APIRouter, Depends, HTTPException
from typing import List


from sqlmodel import Session, select
from app.models.users import User
from app.models.game import Game


from app.schemas.game import GameCreate, GameDetailResponse, GameSimpleResponse, GameUpdate

from app.core.dependencies import SessionDep
from app.core.dependencies_auth import AdminUser
from app.core.dependencies_game import get_game_service

from app.services.rawg_service import buscar_jogos_rawg
from app.services.rawg_import_service import importar_jogos_rawg
from app.services.game_service import GameService
router = APIRouter(prefix="/games",tags=["Games"])


# @router.delete("/{id}")
# def delete_papel(id: int, session: SessionDep)-> None:
#     papel = session.query(Papel).get(id)
#     session.delete(papel)
#     session.commit()

# @router.put("/{id}",response_model=Papel)
# def update_papel(id: int, papel: Papel, session: SessionDep)-> Papel:
#     papel_db= session.query(Papel).get(id)
#     if papel_db is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Papel não encontrado")
#     for key, value in papel.model_dump(exclude_unset=True).items():
#         setattr(papel_db, key, value)
#     session.add(papel_db)
#     session.commit()
#     session.refresh(papel_db)
#     session.commit()
#     return papel_db


@router.post("/")
def criar_jogo(
    game: Game,
    user: AdminUser,
    service: GameService = Depends(get_game_service),
):
    service.criar_jogos(game)
    return {
        "message": f"Jogo (id:{game.jgs_id}) cadastrado com sucesso!",
        "id": game.jgs_id,
    }

@router.get("/")
def listar_jogos(
    service: GameService = Depends(get_game_service),
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


@router.get("/{game_id}", response_model=Game)
def get_game_by_id(game_id: int, session: SessionDep) -> Game:
    game = session.get(Game, game_id)

    if not game:
        raise HTTPException(
            status_code=404,
            detail="Jogo não encontrado",
        )

    return game