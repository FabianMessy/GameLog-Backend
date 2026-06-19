from app.core.dependencies import SessionDep

from app.services.game_service import GameService
from app.services.game_service import GameServiceImpl


def get_game_service(
    session: SessionDep
) -> GameService:

    return GameServiceImpl(session)