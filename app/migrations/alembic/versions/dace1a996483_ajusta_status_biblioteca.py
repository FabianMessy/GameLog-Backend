"""ajusta enum de status da biblioteca (RF008)

Revision ID: dace1a996483
Revises: b32a990d459e
Create Date: 2026-09-09 00:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'dace1a996483'
down_revision: Union[str, Sequence[str], None] = 'b32a990d459e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


OLD_ENUM = sa.Enum(
    'JOGANDO', 'COMPLETO', 'PAUSADO', 'ABANDONADO', 'PLANEJADO',
    name='librarystatus',
)
# Enum "largo": união do antigo com o novo. É um passo intermediário —
# nunca fica assim de verdade, só existe pra dar espaço da coluna
# aceitar os dois vocabulários enquanto os dados são migrados.
WIDE_ENUM = sa.Enum(
    'JOGANDO', 'COMPLETO', 'PAUSADO', 'ABANDONADO', 'PLANEJADO', 'FINALIZADO',
    name='librarystatus',
)
NEW_ENUM = sa.Enum(
    'PLANEJADO', 'JOGANDO', 'FINALIZADO', 'ABANDONADO',
    name='librarystatus',
)


def upgrade() -> None:
    """Upgrade schema."""
    # RF008 do documento de requisitos define só 4 status (Quero
    # jogar, Jogando, Finalizado, Abandonado). O enum tinha "Pausado"
    # sobrando e "Completo" em vez de "Finalizado". Decisão de equipe
    # em 04/09/2026: ajustar o código pro documento.
    #
    # Estreitar o enum direto (ALTER de OLD pra NEW numa tacada só)
    # quebraria qualquer linha que já estivesse com 'COMPLETO' ou
    # 'PAUSADO' — o MySQL não dá erro nisso, ele silenciosamente troca
    # o valor inválido por uma string vazia, o que corrompe o dado sem
    # avisar. Por isso o ALTER acontece em 3 passos: alarga o enum,
    # migra os valores existentes, só depois estreita pro definitivo.
    op.alter_column(
        'tb_biblioteca',
        'bib_status',
        existing_type=OLD_ENUM,
        type_=WIDE_ENUM,
        existing_nullable=False,
    )

    # 'COMPLETO' só foi renomeado — dado equivalente, migra direto.
    op.execute(
        "UPDATE tb_biblioteca SET bib_status = 'FINALIZADO' "
        "WHERE bib_status = 'COMPLETO'"
    )
    # 'PAUSADO' não tem equivalente no RF008 novo. Decisão do time:
    # mapear pra 'JOGANDO' — um jogo pausado ainda está, na prática,
    # "em andamento" entre as 4 opções que sobraram (a alternativa
    # seria 'ABANDONADO', mas isso mudaria o sentido de forma mais
    # drástica pro usuário que só pausou temporariamente).
    op.execute(
        "UPDATE tb_biblioteca SET bib_status = 'JOGANDO' "
        "WHERE bib_status = 'PAUSADO'"
    )

    op.alter_column(
        'tb_biblioteca',
        'bib_status',
        existing_type=WIDE_ENUM,
        type_=NEW_ENUM,
        existing_nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        'tb_biblioteca',
        'bib_status',
        existing_type=NEW_ENUM,
        type_=WIDE_ENUM,
        existing_nullable=False,
    )

    op.execute(
        "UPDATE tb_biblioteca SET bib_status = 'COMPLETO' "
        "WHERE bib_status = 'FINALIZADO'"
    )
    # 'PAUSADO' não volta: a distinção entre "pausado" e "jogando" já
    # tinha sido perdida na subida (os dois viraram 'JOGANDO'), então
    # não tem como reconstruir qual linha era qual. Isso é esperado —
    # downgrade de uma migration que funde dois valores num só nunca é
    # perfeitamente simétrico.

    op.alter_column(
        'tb_biblioteca',
        'bib_status',
        existing_type=WIDE_ENUM,
        type_=OLD_ENUM,
        existing_nullable=False,
    )
