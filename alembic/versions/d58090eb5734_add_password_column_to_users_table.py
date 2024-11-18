"""Add password column to users table

Revision ID: d58090eb5734
Revises: 0d35f3996a83
Create Date: 2024-11-18 20:20:05.540934

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
# revision identifiers, used by Alembic.
revision: str = 'd58090eb5734'
down_revision: Union[str, None] = '0d35f3996a83'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password', sa.String(), nullable=False, server_default='default_password'))
    # ### end Alembic commands ###

    # Remove the default value after the column is added
    op.alter_column('users', 'password', server_default=None)


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'password')
    # ### end Alembic commands ###