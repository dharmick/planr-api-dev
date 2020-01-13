"""empty message

Revision ID: 35f4c41849d0
Revises: 344c88d5dc9b
Create Date: 2020-01-09 14:47:11.170050

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '35f4c41849d0'
down_revision = '344c88d5dc9b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pois', sa.Column('description', sa.String(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('pois', 'description')
    # ### end Alembic commands ###