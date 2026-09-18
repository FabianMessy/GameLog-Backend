from sqlmodel import Session, select
from sqlalchemy import and_
from app.models.game import Game
from app.models.genre import Genre
from app.models.game_genre import GameGenre
from app.schemas.library import LibraryFilters

from app.models.library import Library

class LibraryRepository:

    def __init__(self, session: Session):
        self.session = session

    def create(self, library: Library) -> Library:
        self.session.add(library)
        self.session.commit()
        self.session.refresh(library)
        return library

    def get_by_id(self, bib_id: int) -> Library | None:
        statement = select(Library).where(
            Library.bib_id == bib_id
        )
        return self.session.exec(statement).first()

    def get_by_user(
        self,
        user_id: int,
        filtros: LibraryFilters | None = None
    ) -> list[Library]:

        statement = (
            select(Library)
            .join(Game, Game.jgs_id == Library.bib_jgs_id)
            .where(Library.bib_usr_id == user_id)
        )

        if filtros:
            if filtros.avaliacao_min is not None:
                statement = statement.where(
                    Library.bib_usr_nota >= filtros.avaliacao_min
                )

            if filtros.avaliacao_max is not None:
                statement = statement.where(
                    Library.bib_usr_nota <= filtros.avaliacao_max
                )

            if filtros.lancamento_inicio:
                statement = statement.where(
                    Game.jgs_lancamento >= filtros.lancamento_inicio
                )

            if filtros.lancamento_fim:
                statement = statement.where(
                    Game.jgs_lancamento <= filtros.lancamento_fim
                )

            if filtros.status:
                statement = statement.where(
                    Library.bib_status.in_(filtros.status)
                )

            if filtros.horas_min is not None:
                statement = statement.where(
                    Library.bib_jgs_horas_jogadas >= filtros.horas_min
                )

            if filtros.horas_max is not None:
                statement = statement.where(
                    Library.bib_jgs_horas_jogadas <= filtros.horas_max
                )

            if filtros.classificacoes:
                statement = statement.where(
                    Game.jgs_classificacao_indicativa.in_(filtros.classificacoes)
                )

            if filtros.generos:
                statement = statement.join(
                    GameGenre,
                    GameGenre.jgs_id == Game.jgs_id
                ).join(
                    Genre,
                    Genre.gen_id == GameGenre.gen_id
                ).where(
                    Genre.gen_nome.in_(filtros.generos)
                )

        return self.session.exec(statement.distinct()).all()

    def get_by_user_and_game(
        self,
        user_id: int,
        game_id: int
    ) -> Library | None:

        statement = select(Library).where(
            Library.bib_usr_id == user_id,
            Library.bib_jgs_id == game_id
        )

        return self.session.exec(statement).first()

    def get_reviews_by_game(self, game_id: int) -> list[Library]:
        # RF013: só entram aqui entradas com review escrita (texto em
        # bib_usr_avaliacao). Quem só deu nota, sem escrever nada, não
        # aparece como "review" na página de detalhes — a nota geral
        # do jogo (jgs_nota_media) já cobre esse caso agregado.
        statement = (
            select(Library)
            .where(
                Library.bib_jgs_id == game_id,
                Library.bib_usr_avaliacao.is_not(None),
            )
            .order_by(Library.bib_updated_at.desc())
        )
        return self.session.exec(statement).all()

    def update(self, library: Library) -> Library:
        self.session.add(library)
        self.session.commit()
        self.session.refresh(library)
        return library

    def delete(self, library: Library) -> None:
        self.session.delete(library)
        self.session.commit()
