"""Adding new column

Revision ID: 06e5ab206847
Revises: 0d4dc06997ac
Create Date: 2025-03-30 21:46:14.158629

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '06e5ab206847'
down_revision: Union[str, None] = '0d4dc06997ac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))


def downgrade() -> None:
   op.drop_column('posts','content')
