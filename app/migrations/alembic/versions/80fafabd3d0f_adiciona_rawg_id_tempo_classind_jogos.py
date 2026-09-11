"""adiciona jgs_rawg_id, jgs_tempo_medio_horas e jgs_classificacao_indicativa em tb_jogos

Revision ID: 80fafabd3d0f
Revises: dace1a996483
Create Date: 2026-09-09 00:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = '80fafabd3d0f'
down_revision: Union[str, Sequence[str], None] = 'dace1a996483'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Três colunas novas em tb_jogos, todas alimentadas na importação
    # de um jogo da RAWG (rawg_import_service.py):
    #
    # - jgs_rawg_id: antes um jogo importado só era identificável pelo
    #   título — não tinha como voltar de "jogo salvo no banco" pra
    #   "jogo na RAWG" de forma confiável. Esse é o id que já vem na
    #   resposta da RAWG, guardado direto.
    # - jgs_tempo_medio_horas: tempo médio de conclusão do jogo (dado
    #   geral, tipo HowLongToBeat — não é o tempo jogado por um
    #   usuário). Alimenta o filtro "Tempo de Jogo" da Biblioteca.
    # - jgs_classificacao_indicativa: aproximação da classificação
    #   ClassInd a partir do ESRB da RAWG (a RAWG não tem ClassInd, e
    #   nem todo jogo tem ESRB preenchido). Alimenta o filtro
    #   "Classificação Indicativa" da Biblioteca.
    #
    # As três são colunas novas e opcionais (nullable=True) — não muda
    # o tipo nem a obrigatoriedade de nada que já existia, então não
    # precisa mexer em dado nenhum: toda linha que já existir em
    # tb_jogos simplesmente passa a ter esses três campos como NULL,
    # o que é um valor válido pra eles.
    op.add_column(
        'tb_jogos',
        sa.Column('jgs_rawg_id', sa.Integer(), nullable=True),
    )
    op.create_index(
        op.f('ix_tb_jogos_jgs_rawg_id'),
        'tb_jogos',
        ['jgs_rawg_id'],
        unique=True,
    )

    op.add_column(
        'tb_jogos',
        sa.Column('jgs_tempo_medio_horas', sa.Integer(), nullable=True),
    )
    op.add_column(
        'tb_jogos',
        sa.Column('jgs_classificacao_indicativa', sa.String(length=10), nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('tb_jogos', 'jgs_classificacao_indicativa')
    op.drop_column('tb_jogos', 'jgs_tempo_medio_horas')
    op.drop_index(op.f('ix_tb_jogos_jgs_rawg_id'), table_name='tb_jogos')
    op.drop_column('tb_jogos', 'jgs_rawg_id')
