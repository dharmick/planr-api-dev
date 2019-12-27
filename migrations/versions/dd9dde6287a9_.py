"""empty message

Revision ID: dd9dde6287a9
Revises: ca4e1d345132
Create Date: 2019-12-23 17:58:55.385190

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd9dde6287a9'
down_revision = 'ca4e1d345132'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pois', sa.Column('average_rating', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('pois', 'average_rating')
    # ### end Alembic commands ###