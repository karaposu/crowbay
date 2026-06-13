"""clarifier_runs.tos_category (ToS matrix v1 ratified — full-coverage logging)

Revision ID: b7d31f8c4e22
Revises: a41c7e9d2b10
Create Date: 2026-06-12 15:20:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b7d31f8c4e22'
down_revision: Union[str, Sequence[str], None] = 'a41c7e9d2b10'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('clarifier_runs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tos_category', sa.String(length=16), nullable=True))
        batch_op.create_index(batch_op.f('ix_clarifier_runs_tos_category'), ['tos_category'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('clarifier_runs', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_clarifier_runs_tos_category'))
        batch_op.drop_column('tos_category')
