"""Add tags to projects and tasks

Revision ID: 0d35f3996a83
Revises: 9621d195d4e2
Create Date: 2024-11-14 13:22:57.110368

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0d35f3996a83'
down_revision: Union[str, None] = '9621d195d4e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('projects', sa.Column('tags', sa.Text(), nullable=True))
    op.add_column('tasks', sa.Column('tags', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tasks', 'tags')
    op.drop_column('projects', 'tags')
    # ### end Alembic commands ###
