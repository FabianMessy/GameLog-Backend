from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.user import UserCreate
from app.core.dependencies_auth import CurrentUser
from app.core.dependencies_user import get_user_service
from app.services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register(
    user: UserCreate,
    service: Annotated[UserService, Depends(get_user_service)],
):
    service.registrar(user)
    return {
        "message": "Usuário registrado com sucesso!"
    }


@router.post("/login")
def login(
    service: Annotated[UserService, Depends(get_user_service)],
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    token = service.autenticar(form_data.username, form_data.password)

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.get("/me")
def get_me(
    current_user: CurrentUser
):
    return current_user
