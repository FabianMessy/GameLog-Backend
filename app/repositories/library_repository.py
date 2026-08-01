from sqlmodel import Session, select

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

    def get_by_user(self, user_id: int) -> list[Library]:
        statement = select(Library).where(
            Library.bib_usr_id == user_id
        )
        return self.session.exec(statement).all()

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

    def update(self, library: Library) -> Library:
        self.session.add(library)
        self.session.commit()
        self.session.refresh(library)
        return library

    def delete(self, library: Library) -> None:
        self.session.delete(library)
        self.session.commit()