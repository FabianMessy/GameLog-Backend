from typing import Annotated
from fastapi import Depends
from sqlmodel import Session
from app.core.database import get_session
from app.repositories.library_repository import LibraryRepository
from app.services.library_service import LibraryService
from app.services.implementation.library_service_implementation import LibraryServiceImpl


SessionDep = Annotated[Session,Depends(get_session)]


def get_library_repository(
    session: SessionDep,
) -> LibraryRepository:
    return LibraryRepository(session)


# ============================
# Services
# ============================


def get_library_service(
    repository: Annotated[
        LibraryRepository,
        Depends(get_library_repository)
    ],
) -> LibraryService:
    return LibraryServiceImpl(repository)

