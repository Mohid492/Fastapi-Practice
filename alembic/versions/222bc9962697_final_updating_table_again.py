"""Final Updating table again

Revision ID: 222bc9962697
Revises: 1907bfbb488c
Create Date: 2025-03-30 22:13:50.360740

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '222bc9962697'
down_revision: Union[str, None] = '1907bfbb488c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))

def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')

