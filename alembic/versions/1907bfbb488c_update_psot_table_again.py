"""Update psot table again

Revision ID: 1907bfbb488c
Revises: 78949f8db908
Create Date: 2025-03-30 22:05:34.256258

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1907bfbb488c'
down_revision: Union[str, None] = '78949f8db908'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts',
                          referent_table='users', local_cols=['owner_id'], remote_cols=['id'],
                          ondelete='CASCADE')

def downgrade() -> None:
    op.drop_constraint('post_users_fk', 'posts', type_='foreignkey')
    op.drop_column('posts', 'owner_id')
