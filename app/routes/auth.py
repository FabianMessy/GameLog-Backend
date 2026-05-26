from fastapi import APIRouter,Depends,HTTPException,Header
from sqlmodel import Session, select
from app.models.users import User
from app.schemas.user import UserCreate,UserLogin
from app.core.database import get_session
from app.core.security import create_access_token,verify_token
from app.core.dependencies import SessionDep

router = APIRouter( prefix="/auth",tags=["Auth"])


@router.post("/register")
def register(user: UserCreate,session: SessionDep):
    usr_existente = session.exec(select(User).where(    User.usr_email == user.usr_email)).first()

    if usr_existente:
        raise HTTPException(status_code=400,detail="Email já cadastrado")

    usr_novo = User(
        usr_nome_usuario=user.usr_nome_usuario,
        usr_nome_completo=user.usr_nome_completo,
        usr_email=user.usr_email,
        usr_senha=user.usr_senha
    )

    session.add(usr_novo)
    session.commit()
    session.refresh(usr_novo)

    return {
        "message": "Usuário criado com sucesso"
    }


@router.post("/login")
def login(user: UserLogin,session: SessionDep):

    db_user = session.exec( select(User).where(User.usr_email == user.usr_email)).first()

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Email ou senha inválidos"
        )

    if db_user.usr_senha != user.usr_senha:
        raise HTTPException(
            status_code=401,
            detail="Email ou senha inválidos"
        )

    token = create_access_token(
        {
            "user_id": db_user.usr_id,
            "email": db_user.usr_email
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.get("/me")
def get_me(
    authorization: str = Header(None)
):

    print(authorization)

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Token ausente"
        )

    token = authorization.replace(
        "Bearer",
        ""
    )

    payload = verify_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Token inválido"
        )

    return payload