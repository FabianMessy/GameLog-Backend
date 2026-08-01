from typing import Annotated

from fastapi import Depends

from app.core.dependencies import SessionDep
from app.repositories.game_repository import GameRepository
from app.services.game_service import GameService
from app.services.implementation.game_service_implementation import GameServiceImpl


def get_game_repository(
    session: SessionDep,
) -> GameRepository:
    return GameRepository(session)


def get_game_service(
    repository: Annotated[
        GameRepository,
        Depends(get_game_repository)
    ],
) -> GameService:
    return GameServiceImpl(repository)
