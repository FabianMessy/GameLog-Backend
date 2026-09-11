from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.schemas.game import (
    GameCreate,
    GameDetailResponse,
    GameSimpleResponse,
    GameUpdate,
)
from app.schemas.library import LibraryDetailResponse

from app.core.dependencies import SessionDep
from app.core.dependencies_auth import AdminUser, CurrentUser
from app.core.dependencies_game import get_game_service

from app.services.rawg_service import (
    buscar_detalhes_jogo_rawg,
    buscar_jogos_rawg,
    listar_jogos_rawg,
)
from app.services.rawg_import_service import (
    buscar_jogo_local_por_rawg_id,
    importar_jogos_rawg,
    obter_ou_criar_jogo_por_rawg_id,
)
from app.repositories.library_repository import LibraryRepository
from app.services.game_service import GameService

router = APIRouter(prefix="/games", tags=["Games"])


@router.post("/")
def criar_jogo(
    dados: GameCreate,
    user: AdminUser,
    service: Annotated[GameService, Depends(get_game_service)],
):
    jogo = service.criar_jogo(dados)
    return {
        "message": f"Jogo (id:{jogo.jgs_id}) cadastrado com sucesso!",
        "id": jogo.jgs_id,
    }


@router.get("/", response_model=list[GameSimpleResponse])
def listar_jogos(
    service: Annotated[GameService, Depends(get_game_service)],
):
    return service.listar_jogos()


@router.get("/rawg/search")
def buscar_na_rawg(
    nome: str,
    page_size: int = 10,
    page: int = 1,
):
    try:
        return buscar_jogos_rawg(
            nome=nome,
            page_size=page_size,
            page=page,
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/rawg/lista")
def listar_jogos_da_rawg(
    nome: str | None = None,
    genero: str | None = None,
    tag: str | None = None,
    ordering: str | None = None,
    page: int = 1,
    page_size: int = 20,
):
    """
    Lista jogos direto da RAWG (sem exigir 'nome' e sem tocar no banco
    local) — é o que alimenta o catálogo: destaques, categorias e busca
    usam essa mesma rota, só variando os parâmetros.
    """
    try:
        return listar_jogos_rawg(
            nome=nome,
            genero=genero,
            tag=tag,
            ordering=ordering,
            page=page,
            page_size=page_size,
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/rawg/{rawg_id}")
def detalhes_do_jogo_rawg(rawg_id: int):
    """
    Detalhes de um jogo direto da RAWG (não é o mesmo endpoint de
    /games/{game_id}, que busca no banco local). Alimenta a página de
    detalhes do jogo.
    """
    try:
        return buscar_detalhes_jogo_rawg(rawg_id)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get(
    "/rawg/{rawg_id}/minha-biblioteca",
    response_model=LibraryDetailResponse | None,
)
def minha_entrada_biblioteca_do_jogo(
    rawg_id: int,
    session: SessionDep,
    user: CurrentUser,
):
    """
    Diz se ESTE usuário já tem esse jogo (da RAWG) na biblioteca dele —
    e devolve a entrada, se tiver. É o que a página de detalhes usa pra
    decidir entre mostrar "Adicionar à Biblioteca" ou o formulário de
    nota/review/horas.

    Não importa o jogo pro banco só por causa dessa consulta: se ele
    nunca foi importado (nem por este nem por outro usuário), a
    resposta já é `null` sem nem chegar a olhar a tabela de biblioteca
    — afinal, se o jogo não existe localmente, ninguém pode ter
    adicionado ele ainda.
    """
    try:
        jogo = buscar_jogo_local_por_rawg_id(session, rawg_id)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    if not jogo:
        return None

    repo = LibraryRepository(session)
    return repo.get_by_user_and_game(user.usr_id, jogo.jgs_id)


@router.post("/rawg/{rawg_id}/importar-um", response_model=GameSimpleResponse)
def importar_um_jogo_da_rawg(
    rawg_id: int,
    session: SessionDep,
    user: CurrentUser,
):
    """
    Garante que o jogo da RAWG exista em tb_jogos e devolve o registro
    local (com jgs_id) — é o passo que roda antes de POST /library
    quando o usuário clica em "Adicionar à Biblioteca" num jogo que
    veio do catálogo (RAWG), que ainda não tem id local. Qualquer
    usuário logado pode chamar (diferente de /rawg/importar, que é só
    admin), porque aqui só materializa o UM jogo que a pessoa está
    tentando adicionar, não faz import em massa.
    """
    try:
        return obter_ou_criar_jogo_por_rawg_id(session, rawg_id)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/rawg/importar")
def importar_rawg_para_banco(
    session: SessionDep,
    user: AdminUser,
    search: str | None = None,
    pages: int = 1,
    page_size: int = 10,
):
    try:
        return importar_jogos_rawg(
            session=session,
            search=search,
            pages=pages,
            page_size=page_size,
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/{game_id}", response_model=GameDetailResponse)
def get_game_by_id(
    game_id: int,
    service: Annotated[GameService, Depends(get_game_service)],
):
    return service.buscar_por_id(game_id)


@router.put("/{game_id}", response_model=GameDetailResponse)
def atualizar_jogo(
    game_id: int,
    dados: GameUpdate,
    user: AdminUser,
    service: Annotated[GameService, Depends(get_game_service)],
):
    return service.atualizar(game_id, dados)


@router.delete("/{game_id}", status_code=204)
def remover_jogo(
    game_id: int,
    user: AdminUser,
    service: Annotated[GameService, Depends(get_game_service)],
):
    service.remover(game_id)
