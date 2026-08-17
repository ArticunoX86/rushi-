"""merge multiple heads

Revision ID: 023ae7e47788
Revises: 021f0a083b84, d1e2f3a4b5c6
Create Date: 2026-08-17 16:51:03.041129

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '023ae7e47788'
down_revision: Union[str, Sequence[str], None] = ('021f0a083b84', 'd1e2f3a4b5c6')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
