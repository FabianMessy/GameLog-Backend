from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, session
from app.models.users import User
from app.schemas.game import GameCreate, GameDetailResponse, GameSimpleResponse, GameUpdate
from app.models.game import Game
from app.core.dependencies import SessionDep
from app.core.dependencies_auth import AdminUser
from app.services.rawg_service import buscar_jogos_rawg
from services.game_service import GameService
from typing import List

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

@router.post("/", response_model=Game)
def criar_jogo(game: Game, user: AdminUser, service: GameService):
    service.criar_jogos(game)
    return {
            "message": f"Jogo (id:{game.jgs_id}) cadastrado com sucesso!",
            "id": game.jgs_id
            }
    

@router.get("/", response_model=List[Game])
def listar_jogos(service: GameService) -> List[Game]:

    return service.listar_jogos()

@router.get("/rawg/search")
def buscar_na_rawg(nome: str):
    resultado = buscar_jogos_rawg(nome)

    if not resultado:
        raise HTTPException(
            status_code=500,
            detail="Erro ao buscar jogos na RAWG"
        )

    return resultado

@router.get("/{game_id}", response_model=Game)
def get_game_by_id(game_id: int, session: SessionDep) -> Game:
    game = session.get(Game, game_id)

    if not game:
        raise HTTPException(
            status_code=404,
            detail="Jogo não encontrado"
        )

    return game