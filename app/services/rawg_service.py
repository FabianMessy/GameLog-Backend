from __future__ import annotations

from typing import Any

import httpx

from app.core.config import RAWG_API_KEY

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


def listar_jogos_rawg(page_size: int = 20, page: int = 1):
    return _request_rawg(
        "games",
        {
            "page_size": page_size,
            "page": page,
            "ordering": "-rating",
        },
    )


def buscar_detalhes_jogo_rawg(rawg_id: int):
    return _request_rawg(f"games/{rawg_id}")
