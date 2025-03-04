"""Initial migration

Revision ID: 8d1b48468dba
Revises: 0c60f3d8b245
Create Date: 2025-02-19 15:53:04.911295

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8d1b48468dba'
down_revision: Union[str, None] = '0c60f3d8b245'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('quantity', sa.Integer(), nullable=True))
    op.drop_column('orders', 'stock')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('stock', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('orders', 'quantity')
    # ### end Alembic commands ###
