from fastapi import HTTPException

from app.models.game import Game
from app.repositories.game_repository import GameRepository
from app.schemas.game import GameCreate, GameUpdate
from app.services.game_service import GameService


class GameServiceImpl(GameService):

    def __init__(self, repository: GameRepository):
        self.repository = repository

    def criar_jogo(self, dados: GameCreate) -> Game:
        jogo_existente = self.repository.get_by_titulo_e_desenvolvedor(
            dados.jgs_titulo,
            dados.jgs_desenvolvedor
        )

        if jogo_existente:
            raise HTTPException(
                status_code=400,
                detail="Jogo já cadastrado"
            )

        novo_jogo = Game(
            jgs_titulo=dados.jgs_titulo,
            jgs_descricao=dados.jgs_descricao,
            jgs_lancamento=dados.jgs_lancamento,
            jgs_desenvolvedor=dados.jgs_desenvolvedor,
            jgs_distribuidor=dados.jgs_distribuidor,
            jgs_capa_url=str(dados.jgs_capa_url) if dados.jgs_capa_url else None,
        )

        return self.repository.create(novo_jogo)

    def listar_jogos(self) -> list[Game]:
        return self.repository.list_all()

    def buscar_por_id(self, game_id: int) -> Game:
        jogo = self.repository.get_by_id(game_id)

        if not jogo:
            raise HTTPException(
                status_code=404,
                detail="Jogo não encontrado"
            )

        return jogo

    def atualizar(self, game_id: int, dados: GameUpdate) -> Game:
        jogo = self.buscar_por_id(game_id)

        update = dados.model_dump(exclude_unset=True)

        for campo, valor in update.items():
            if campo == "jgs_capa_url" and valor is not None:
                valor = str(valor)
            setattr(jogo, campo, valor)

        return self.repository.update(jogo)

    def remover(self, game_id: int) -> None:
        jogo = self.buscar_por_id(game_id)
        self.repository.delete(jogo)
