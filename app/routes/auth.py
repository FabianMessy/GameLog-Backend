from fastapi import APIRouter,Depends,HTTPException,Header
from sqlmodel import Session, select
from app.models.users import User
from app.schemas.user import UserCreate,UserLogin
from app.core.database import get_session
from app.core.security import create_access_token,verify_token, hash_password, verify_password, oauth2_scheme
from app.core.dependencies import SessionDep
from app.core.dependencies_auth import AdminUser, CurrentUser

router = APIRouter( prefix="/auth",tags=["Auth"])

@router.post("/register")
def register(user: UserCreate, session: SessionDep):
    usr_existente = session.exec(select(User).where(User.usr_email == user.usr_email)).first()

    if usr_existente:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    usr_novo = User(
        usr_nome_usuario=user.usr_nome_usuario,
        usr_nome_completo=user.usr_nome_completo,
        usr_email=user.usr_email,
        usr_senha=hash_password(user.usr_senha),

        usr_bio=user.usr_bio,
        usr_avatar_url=user.usr_avatar_url
    )

    session.add(usr_novo)
    session.commit()
    session.refresh(usr_novo)

    return {
        "message": "Usuário registrado com sucesso!"
    }


@router.post("/login")
def login(user: UserLogin, session: SessionDep):

    db_user = session.exec(select(User).where(User.usr_email == user.usr_email)).first()

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Email ou senha inválidos"
        )

    if not verify_password(
        user.usr_senha,
        db_user.usr_senha
    ):
        raise HTTPException(
            status_code=401,
            detail="Email ou senha inválidos"
        )

    token = create_access_token(
        {
            "user_id": db_user.usr_id,
            "email": db_user.usr_email,
            "admin": db_user.usr_admin
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.get("/me")
def get_me(
    current_user: CurrentUser
):
    return current_user