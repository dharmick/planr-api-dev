"""empty message

Revision ID: e5e8274a903e
Revises: 9c0cb5271326
Create Date: 2020-01-03 13:36:28.353414

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5e8274a903e'
down_revision = '9c0cb5271326'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cities', sa.Column('description', sa.String(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('cities', 'description')
    # ### end Alembic commands ###
