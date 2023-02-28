"""add cookie for user

Revision ID: 9af5db5a8b91
Revises: 78a33ea3220d
Create Date: 2023-02-23 02:49:15.521621

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9af5db5a8b91'
down_revision = '78a33ea3220d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('cookies', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'cookies')
    # ### end Alembic commands ###