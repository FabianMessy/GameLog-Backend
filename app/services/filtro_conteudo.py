"""
Regras de conteúdo do GameLog: o que nunca deve aparecer no site e qual
classificação indicativa vale quando a RAWG não informa nenhuma.

Fica num módulo só para as duas regras valerem igual em todo lugar: catálogo,
pesquisa, detalhes, importação, jogos salvos e biblioteca.
"""

from typing import Any

# Se o NOME do jogo tiver qualquer um destes termos (sem diferenciar
# maiúsculas de minúsculas), o jogo é escondido do site inteiro.
TERMOS_BLOQUEADOS_NO_TITULO = (
    "hentai", "porn", "xxx", "nsfw", "r18", "r-18",
    "erotic", "eroge", "ecchi", "lewd", "doujin", "yaoi",
    "sexy", "sexual", "fetish", "bdsm", "futanari",
    "striptease", "stripper", "nympho", "orgasm", "masturbat",
    "blowjob", "gangbang", "bukkake", "creampie", "cumshot",
    "slut", "whore", "vagina", "nipple",
    "uncensored", "xvideos", "pornhub", "onlyfans",
    "putaria", "lolicon", "shotacon", "rapelay",
    "incest", "bestiality", "pedophil",
)

# Classificação usada quando a RAWG não informa ESRB (mesmo rótulo do
# _ESRB_PARA_CLASSIND em rawg_import_service.py).
CLASSIFICACAO_PADRAO = "+18"


class JogoBloqueadoError(Exception):
    """Lançada quando alguém tenta abrir ou adicionar um jogo bloqueado."""


def titulo_bloqueado(titulo: str | None) -> bool:
    """Diz se o título tem algum dos termos bloqueados."""
    texto = (titulo or "").casefold()
    return any(termo in texto for termo in TERMOS_BLOQUEADOS_NO_TITULO)


def remover_jogos_bloqueados(jogos: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Tira de uma lista de jogos da RAWG os que têm título bloqueado."""
    return [j for j in jogos if not titulo_bloqueado(j.get("name"))]
