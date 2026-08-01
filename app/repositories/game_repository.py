from sqlmodel import Session, select

from app.models.game import Game


class GameRepository:

    def __init__(self, session: Session):
        self.session = session

    def create(self, game: Game) -> Game:
        self.session.add(game)
        self.session.commit()
        self.session.refresh(game)
        return game

    def get_by_id(self, game_id: int) -> Game | None:
        statement = select(Game).where(Game.jgs_id == game_id)
        return self.session.exec(statement).first()

    def get_by_titulo_e_desenvolvedor(
        self,
        titulo: str,
        desenvolvedor: str
    ) -> Game | None:

        statement = select(Game).where(
            Game.jgs_titulo == titulo,
            Game.jgs_desenvolvedor == desenvolvedor
        )

        return self.session.exec(statement).first()

    def list_all(self) -> list[Game]:
        return self.session.exec(select(Game)).all()

    def update(self, game: Game) -> Game:
        self.session.add(game)
        self.session.commit()
        self.session.refresh(game)
        return game

    def delete(self, game: Game) -> None:
        self.session.delete(game)
        self.session.commit()
