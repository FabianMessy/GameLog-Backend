from fastapi import APIRouter,Depends,HTTPException
from sqlmodel import Session,select
from app.models.game import Game
from app.core.dependencies import SessionDep

router = APIRouter(prefix="/games",tags=["Games"])


@router.get("/")
def listar_jogos(session: SessionDep):

    games = session.exec(select(Game)).all()

    return games


@router.get("/{game_id}")
def get_game(game_id: int,session: SessionDep):
    game = session.get(Game,game_id)

    if not game:
        raise HTTPException(
            status_code=404,
            detail="Jogo não encontrado"
        )

    return game