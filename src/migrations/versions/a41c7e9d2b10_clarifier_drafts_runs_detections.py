"""clarifier drafts, runs, detection records + task normalized_slots

Revision ID: a41c7e9d2b10
Revises: f033a367fa75
Create Date: 2026-06-12 15:05:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a41c7e9d2b10'
down_revision: Union[str, Sequence[str], None] = 'f033a367fa75'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('task_drafts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.Column('payload', sa.JSON(), nullable=False),
    sa.Column('status', sa.String(length=20), nullable=False),
    sa.Column('idempotency_key', sa.String(length=120), nullable=True),
    sa.Column('task_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], name=op.f('fk_task_drafts_owner_id_users')),
    sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], name=op.f('fk_task_drafts_task_id_tasks')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_task_drafts')),
    sa.UniqueConstraint('idempotency_key', name=op.f('uq_task_drafts_idempotency_key'))
    )
    with op.batch_alter_table('task_drafts', schema=None) as batch_op:
        batch_op.create_index('ix_task_drafts_owner_created', ['owner_id', 'created_at'], unique=False)
        batch_op.create_index(batch_op.f('ix_task_drafts_owner_id'), ['owner_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_task_drafts_status'), ['status'], unique=False)

    op.create_table('clarifier_runs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('draft_id', sa.Integer(), nullable=False),
    sa.Column('submission_hash', sa.String(length=64), nullable=False),
    sa.Column('catalog_version', sa.String(length=16), nullable=False),
    sa.Column('backend', sa.String(length=16), nullable=False),
    sa.Column('status', sa.String(length=16), nullable=False),
    sa.Column('llm_output', sa.JSON(), nullable=True),
    sa.Column('card_payload', sa.JSON(), nullable=True),
    sa.Column('normalized_slots', sa.JSON(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['draft_id'], ['task_drafts.id'], name=op.f('fk_clarifier_runs_draft_id_task_drafts')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_clarifier_runs')),
    sa.UniqueConstraint('draft_id', 'submission_hash', name='uq_clarifier_runs_draft_hash')
    )
    with op.batch_alter_table('clarifier_runs', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_clarifier_runs_draft_id'), ['draft_id'], unique=False)

    op.create_table('detection_records',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('run_id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=12), nullable=False),
    sa.Column('entry_version', sa.Integer(), nullable=False),
    sa.Column('result', sa.String(length=16), nullable=False),
    sa.Column('severity_at_fire', sa.String(length=10), nullable=True),
    sa.Column('response_shown', sa.JSON(), nullable=True),
    sa.Column('resolution', sa.String(length=20), nullable=True),
    sa.Column('resolution_value', sa.JSON(), nullable=True),
    sa.ForeignKeyConstraint(['run_id'], ['clarifier_runs.id'], name=op.f('fk_detection_records_run_id_clarifier_runs')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_detection_records'))
    )
    with op.batch_alter_table('detection_records', schema=None) as batch_op:
        batch_op.create_index('ix_detection_records_code_result', ['code', 'result'], unique=False)
        batch_op.create_index(batch_op.f('ix_detection_records_run_id'), ['run_id'], unique=False)

    with op.batch_alter_table('tasks', schema=None) as batch_op:
        batch_op.add_column(sa.Column('normalized_slots', sa.JSON(), nullable=True))
        batch_op.add_column(sa.Column('clarifier_run_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            batch_op.f('fk_tasks_clarifier_run_id_clarifier_runs'),
            'clarifier_runs', ['clarifier_run_id'], ['id'],
        )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('tasks', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_tasks_clarifier_run_id_clarifier_runs'), type_='foreignkey')
        batch_op.drop_column('clarifier_run_id')
        batch_op.drop_column('normalized_slots')

    with op.batch_alter_table('detection_records', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_detection_records_run_id'))
        batch_op.drop_index('ix_detection_records_code_result')
    op.drop_table('detection_records')

    with op.batch_alter_table('clarifier_runs', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_clarifier_runs_draft_id'))
    op.drop_table('clarifier_runs')

    with op.batch_alter_table('task_drafts', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_task_drafts_status'))
        batch_op.drop_index(batch_op.f('ix_task_drafts_owner_id'))
        batch_op.drop_index('ix_task_drafts_owner_created')
    op.drop_table('task_drafts')
