from __future__ import annotations

from typing import Any

import httpx

from app.core.config import settings

RAWG_API_KEY = settings.RAWG_API_KEY

RAWG_BASE_URL = "https://api.rawg.io/api"


class RawgConfigError(RuntimeError):
    pass


class RawgRequestError(RuntimeError):
    pass


def _request_rawg(endpoint: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    if not RAWG_API_KEY:
        raise RawgConfigError("RAWG_API_KEY não configurada no arquivo .env")

    url = f"{RAWG_BASE_URL}/{endpoint.lstrip('/')}"
    request_params = {"key": RAWG_API_KEY}
    if params:
        request_params.update(params)

    try:
        response = httpx.get(url, params=request_params, timeout=20)
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        status = exc.response.status_code
        try:
            detail = exc.response.json()
        except Exception:
            detail = exc.response.text
        raise RawgRequestError(f"Erro HTTP {status} na RAWG: {detail}") from exc
    except httpx.HTTPError as exc:
        raise RawgRequestError(f"Erro de conexão com a RAWG: {exc}") from exc

    return response.json()


def buscar_jogos_rawg(nome: str, page_size: int = 10, page: int = 1):
    return _request_rawg(
        "games",
        {
            "search": nome,
            "page_size": page_size,
            "page": page,
        },
    )


def listar_jogos_rawg(
    nome: str | None = None,
    genero: str | None = None,
    tag: str | None = None,
    ordering: str | None = None,
    page_size: int = 20,
    page: int = 1,
):
    """
    Lista jogos da RAWG sem precisar ter nada salvo no banco local.
    Usada pelo catálogo (destaques, filtro por categoria e busca) — cada
    filtro é opcional, então dá pra chamar sem nenhum argumento pra
    pegar os jogos mais bem avaliados em geral.

    - nome: texto livre (equivalente ao parâmetro "search" da RAWG)
    - genero: slug ou id de gênero da RAWG (ex.: "action", "indie", "rpg")
    - tag: slug ou id de tag da RAWG (ex.: "horror", "co-op")
    - ordering: se não for passado, cai no padrão da RAWG — que é
      ordenar por relevância quando tem "nome" e por id quando não tem.
      Pra navegação sem busca (destaques, categorias) a gente força
      "-rating" aqui embaixo pra não depender do padrão da RAWG. Pra
      busca por nome, NÃO force ordering: forçar "-rating" numa busca
      empurra pra fora resultados relevantes mas com nota baixa/sem
      nota (ex.: "Counter-Strike 2" sumia da primeira página por causa
      disso).
    """
    if ordering is None and not nome:
        ordering = "-rating"

    params: dict[str, Any] = {
        "page_size": page_size,
        "page": page,
    }
    if ordering:
        params["ordering"] = ordering
    if nome:
        params["search"] = nome
    if genero:
        params["genres"] = genero
    if tag:
        params["tags"] = tag

    return _request_rawg("games", params)


def buscar_detalhes_jogo_rawg(rawg_id: int):
    return _request_rawg(f"games/{rawg_id}")
