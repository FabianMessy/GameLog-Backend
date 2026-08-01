from typing import Annotated

from fastapi import Depends

from app.core.dependencies import SessionDep
from app.repositories.users_repository import UsersRepository
from app.services.user_service import UserService
from app.services.implementation.user_service_implementation import UserServiceImpl


def get_users_repository(
    session: SessionDep,
) -> UsersRepository:
    return UsersRepository(session)


def get_user_service(
    repository: Annotated[
        UsersRepository,
        Depends(get_users_repository)
    ],
) -> UserService:
    return UserServiceImpl(repository)
