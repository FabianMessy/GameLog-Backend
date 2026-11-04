from abc import ABC, abstractmethod

from app.models.users import User
from app.schemas.user import UserCreate, UserUpdate


class UserService(ABC):

    @abstractmethod
    def registrar(self, dados: UserCreate) -> User:
        pass

    @abstractmethod
    def autenticar(self, email: str, senha: str) -> str:
        """Retorna o access token JWT quando as credenciais são válidas."""
        pass

    @abstractmethod
    def buscar_por_id(self, user_id: int) -> User:
        pass

    @abstractmethod
    def atualizar(self, user_id: int, dados: UserUpdate) -> User:
        """Atualiza só os campos enviados do perfil do próprio usuário."""
        pass