"""create user set

Revision ID: 2964d8b6ee05
Revises: a58bca99796d
Create Date: 2024-05-06 14:36:44.904000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2964d8b6ee05'
down_revision: Union[str, None] = 'a58bca99796d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
