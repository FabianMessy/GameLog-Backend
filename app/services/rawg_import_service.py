from datetime import date
from typing import Any

from sqlmodel import Session, select

from app.models.game import Game
from app.models.game_genre import GameGenre
from app.models.game_platform import GamePlatform
from app.models.genre import Genre
from app.models.platform import Platform
from app.services.rawg_service import (
    buscar_detalhes_jogo_rawg,
    buscar_jogos_rawg,
    listar_jogos_rawg,
)


def _limitar_texto(valor: str | None, limite: int, padrao: str = "Não informado") -> str:
    texto = (valor or padrao).strip()
    if not texto:
        texto = padrao
    return texto[:limite]


def _converter_data(valor: str | None) -> date:
    if not valor:
        return date.today()

    try:
        return date.fromisoformat(valor)
    except ValueError:
        return date.today()


def _obter_nome_primeiro_item(lista: list[dict[str, Any]] | None) -> str:
    if lista and len(lista) > 0:
        return lista[0].get("name") or "Não informado"
    return "Não informado"


def _get_or_create_genero(session: Session, nome: str) -> Genre:
    nome = _limitar_texto(nome, 50)

    genero = session.exec(
        select(Genre).where(Genre.gen_nome == nome)
    ).first()

    if genero:
        return genero

    genero = Genre(gen_nome=nome)
    session.add(genero)
    session.commit()
    session.refresh(genero)
    return genero


def _get_or_create_plataforma(session: Session, nome: str) -> Platform:
    nome = _limitar_texto(nome, 50)

    plataforma = session.exec(
        select(Platform).where(Platform.plt_nome == nome)
    ).first()

    if plataforma:
        return plataforma

    plataforma = Platform(plt_nome=nome)
    session.add(plataforma)
    session.commit()
    session.refresh(plataforma)
    return plataforma


def _linkar_genero(session: Session, jogo_id: int, genero_id: int) -> None:
    existe = session.exec(
        select(GameGenre).where(
            GameGenre.jgs_id == jogo_id,
            GameGenre.gen_id == genero_id,
        )
    ).first()

    if not existe:
        session.add(GameGenre(jgs_id=jogo_id, gen_id=genero_id))


def _linkar_plataforma(session: Session, jogo_id: int, plataforma_id: int) -> None:
    existe = session.exec(
        select(GamePlatform).where(
            GamePlatform.jgs_id == jogo_id,
            GamePlatform.plt_id == plataforma_id,
        )
    ).first()

    if not existe:
        session.add(GamePlatform(jgs_id=jogo_id, plt_id=plataforma_id))


def importar_jogos_rawg(
    session: Session,
    search: str | None = None,
    pages: int = 1,
    page_size: int = 10,
) -> dict:
    importados = 0
    ignorados = 0
    erros: list[str] = []

    pages = max(1, pages)
    page_size = max(1, min(page_size, 40))

    for page in range(1, pages + 1):
        if search:
            dados = buscar_jogos_rawg(search, page_size=page_size, page=page)
        else:
            dados = listar_jogos_rawg(page_size=page_size, page=page)

        for item in dados.get("results", []):
            rawg_id = item.get("id")
            titulo = _limitar_texto(item.get("name"), 45)

            if not rawg_id or not titulo:
                ignorados += 1
                continue

            ja_existe = session.exec(
                select(Game).where(Game.jgs_titulo == titulo)
            ).first()

            if ja_existe:
                ignorados += 1
                continue

            try:
                detalhes = buscar_detalhes_jogo_rawg(rawg_id)

                desenvolvedor = _obter_nome_primeiro_item(detalhes.get("developers"))
                distribuidor = _obter_nome_primeiro_item(detalhes.get("publishers"))
                descricao = detalhes.get("description_raw") or item.get("name")

                jogo = Game(
                    jgs_titulo=titulo,
                    jgs_descricao=_limitar_texto(descricao, 120),
                    jgs_lancamento=_converter_data(item.get("released")),
                    jgs_desenvolvedor=_limitar_texto(desenvolvedor, 120),
                    jgs_distribuidor=_limitar_texto(distribuidor, 120),
                    jgs_capa_url=_limitar_texto(item.get("background_image"), 255, padrao=""),
                    jgs_nota_media=float(item.get("rating") or 0),
                )

                session.add(jogo)
                session.commit()
                session.refresh(jogo)

                for genero_raw in item.get("genres", []):
                    nome_genero = genero_raw.get("name")
                    if nome_genero:
                        genero = _get_or_create_genero(session, nome_genero)
                        _linkar_genero(session, jogo.jgs_id, genero.gen_id)

                for plataforma_raw in item.get("platforms", []):
                    plataforma_info = plataforma_raw.get("platform") or {}
                    nome_plataforma = plataforma_info.get("name")
                    if nome_plataforma:
                        plataforma = _get_or_create_plataforma(session, nome_plataforma)
                        _linkar_plataforma(session, jogo.jgs_id, plataforma.plt_id)

                session.commit()
                importados += 1
            except Exception as exc:
                session.rollback()
                erros.append(f"{titulo}: {exc}")

    return {
        "importados": importados,
        "ignorados": ignorados,
        "erros": erros,
    }