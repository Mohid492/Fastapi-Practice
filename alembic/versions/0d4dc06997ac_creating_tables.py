"""Creating tables

Revision ID: 0d4dc06997ac
Revises: 
Create Date: 2025-03-30 21:20:29.120512

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0d4dc06997ac'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('posts',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(255), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('posts')
    pass
