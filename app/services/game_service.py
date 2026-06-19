from app.models.game import Game
from abc import ABC, abstractmethod

class GameService(ABC):

    @abstractmethod
    def criar_jogos(self, game: Game):
        pass

    @abstractmethod
    def listar_jogos(self)->list[Game]:
        pass

from sqlmodel import select

from app.models.game import Game

class GameServiceImpl(GameService):

    def __init__(self, session):
        self.session = session

    def criar_jogos(self, game: Game):
        self.session.add(game)
        self.session.commit()
        self.session.refresh(game)

    def listar_jogos(self):
        return self.session.exec(
            select(Game)
        ).all()
