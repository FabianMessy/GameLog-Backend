from sqlmodel import Session, select

from app.models.users import User


class UsersRepository:

    def __init__(self, session: Session):
        self.session = session

    def create(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_by_id(self, user_id: int) -> User | None:
        statement = select(User).where(User.usr_id == user_id)
        return self.session.exec(statement).first()

    def get_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.usr_email == email)
        return self.session.exec(statement).first()

    def get_by_username(self, username: str) -> User | None:
        statement = select(User).where(User.usr_nome_usuario == username)
        return self.session.exec(statement).first()

    def update(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def delete(self, user: User) -> None:
        self.session.delete(user)
        self.session.commit()
