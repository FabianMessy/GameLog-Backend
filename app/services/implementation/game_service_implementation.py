from typing import Annotated
from fastapi import Depends, HTTPException
from sqlmodel import Session, select
from models.game import Game
from services.game_service import Game
from app.core.database import get_session

class GameServiceImpl(Game):

    def __init__(self, session: Annotated[Session, Depends(get_session)]):
        self.session = session

    def criar_jogo(self, session: Annotated[Session, Depends(get_session)], game: Game):
        jogo_existente = session.exec(
            select(Game).where(Game.jgs_titulo == game.jgs_titulo and Game.jgs_desenvolvedor == game.jgs_desenvolvedor)
        ).first()

        if jogo_existente:
            raise HTTPException(
                status_code=400,
                detail="Jogo já cadastrado"
            )

        jogo_novo = Game(
            jgs_capa_url=game.jgs_capa_url,
            jgs_descricao=game.jgs_descricao,
            jgs_desenvolvedor=game.jgs_desenvolvedor,
            jgs_distribuidor=game.jgs_distribuidor,
            jgs_lancamento=game.jgs_lancamento,
            jgs_nota_media=game.jgs_nota_media,
            jgs_titulo=game.jgs_titulo,
        )

        session.add(jogo_novo)
        session.commit()
        session.refresh(jogo_novo)

        return jogo_novo

    def listar_jogos(self)->list[Game]:
        return self.session.query(Game).all()
