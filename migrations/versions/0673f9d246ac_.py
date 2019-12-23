"""empty message

Revision ID: 0673f9d246ac
Revises: dd9dde6287a9
Create Date: 2019-12-23 18:10:38.134931

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0673f9d246ac'
down_revision = 'dd9dde6287a9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('pois', 'name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pois', sa.Column('name', sa.VARCHAR(length=30), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
