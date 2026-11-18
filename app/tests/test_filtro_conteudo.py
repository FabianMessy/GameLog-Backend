"""Testes das regras de conteúdo: jogos bloqueados e classificação padrão."""

from app.schemas.game import GameSimpleResponse
from app.services.filtro_conteudo import (
    CLASSIFICACAO_PADRAO,
    remover_jogos_bloqueados,
    titulo_bloqueado,
)
from app.services.rawg_import_service import _mapear_esrb_para_classind


def test_titulo_com_hentai_e_bloqueado_sem_importar_maiusculas():
    assert titulo_bloqueado("Hentai Heroes")
    assert titulo_bloqueado("super HENTAI world")
    assert titulo_bloqueado("Os Hentais e o Hentai")


def test_titulo_normal_ou_vazio_nao_e_bloqueado():
    assert not titulo_bloqueado("Hollow Knight")
    assert not titulo_bloqueado("")
    assert not titulo_bloqueado(None)


def test_remover_jogos_bloqueados_mantem_a_ordem_dos_demais():
    jogos = [{"name": "A"}, {"name": "Hentai X"}, {"name": "B"}, {}]
    assert [j.get("name") for j in remover_jogos_bloqueados(jogos)] == ["A", "B", None]


def test_sem_esrb_a_classificacao_e_18():
    assert _mapear_esrb_para_classind(None) == "+18"
    assert _mapear_esrb_para_classind({}) == "+18"
    assert _mapear_esrb_para_classind({"name": "Rating Pending"}) == "+18"


def test_esrb_conhecido_continua_mapeado():
    assert _mapear_esrb_para_classind({"name": "Everyone"}) == "Livre"
    assert _mapear_esrb_para_classind({"name": "Teen"}) == "14"


def test_resposta_de_jogo_salvo_sem_classificacao_vira_18():
    dados = dict(
        jgs_id=1,
        jgs_titulo="X",
        jgs_descricao="d",
        jgs_lancamento="2020-01-01",
        jgs_desenvolvedor="a",
        jgs_distribuidor="b",
        jgs_capa_url=None,
        jgs_nota_media=0,
    )
    assert GameSimpleResponse(**dados).jgs_classificacao_indicativa == CLASSIFICACAO_PADRAO
    assert (
        GameSimpleResponse(**dados, jgs_classificacao_indicativa=None).jgs_classificacao_indicativa
        == "+18"
    )
    assert (
        GameSimpleResponse(**dados, jgs_classificacao_indicativa="14").jgs_classificacao_indicativa
        == "14"
    )
