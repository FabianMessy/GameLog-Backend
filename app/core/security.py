import jwt
from datetime import datetime, timedelta
from app.core.config import SECRET_KEY

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

ALGORITHM = "HS256"

# OAuth2
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

# Hash de Senha
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:

    return pwd_context.verify(
        plain_password,
        hashed_password
    )

# Configuração do Token
def create_access_token(data: dict):
    payload = data.copy()

    expire = datetime.utcnow() + timedelta(hours=2)

    payload.update({"exp": expire})

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


def verify_token(token: str):
    print("SECRET_KEY:", SECRET_KEY)
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except Exception as e:
        print(type(e))
        print(e)
        return None