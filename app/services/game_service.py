from models.game import Game
from abc import ABC, abstractmethod

class GameService(ABC):

    @abstractmethod
    def criar_jogos(self, game: Game):
        pass

    @abstractmethod
    def listar_jogos(self)->list[Game]:
        pass
