"""create tasks

Revision ID: d47850c834a4
Revises: 2964d8b6ee05
Create Date: 2024-05-06 14:45:35.168617

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd47850c834a4'
down_revision: Union[str, None] = '2964d8b6ee05'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("title", sa.String, index=True),
        sa.Column("description", sa.String, index=True),
        sa.Column("owner_id", sa.Integer, sa.ForeignKey("users.id")),
    )

    # Adicionar índice na chave estrangeira owner_id
    op.create_index(op.f("ix_tasks_owner_id"), "tasks", ["owner_id"])


def downgrade():
    op.drop_table("tasks")
