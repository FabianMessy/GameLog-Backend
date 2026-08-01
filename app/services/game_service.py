from abc import ABC, abstractmethod

from app.models.game import Game
from app.schemas.game import GameCreate, GameUpdate


class GameService(ABC):

    @abstractmethod
    def criar_jogo(self, dados: GameCreate) -> Game:
        pass

    @abstractmethod
    def listar_jogos(self) -> list[Game]:
        pass

    @abstractmethod
    def buscar_por_id(self, game_id: int) -> Game:
        pass

    @abstractmethod
    def atualizar(self, game_id: int, dados: GameUpdate) -> Game:
        pass

    @abstractmethod
    def remover(self, game_id: int) -> None:
        pass
