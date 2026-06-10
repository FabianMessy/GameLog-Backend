from fastapi import APIRouter,Depends,HTTPException
from sqlmodel import Session,select
from app.models.game import Game
from app.core.dependencies import SessionDep
from app.services.rawg_service import buscar_jogos_rawg

router = APIRouter(prefix="/games",tags=["Games"])


@router.get("/")
def listar_jogos(session: SessionDep):

    games = session.exec(select(Game)).all()

    return games

@router.get("/rawg/search")
def buscar_na_rawg(nome: str):
    resultado = buscar_jogos_rawg(nome)

    if not resultado:
        raise HTTPException(
            status_code=500,
            detail="Erro ao buscar jogos na RAWG"
        )

    return resultado

@router.get("/{game_id}")
def get_game(game_id: int,session: SessionDep):
    game = session.get(Game, game_id)

    if not game:
        raise HTTPException(
            status_code=404,
            detail="Jogo não encontrado"
        )

    return game