"""empty message

Revision ID: 743d6ef273d1
Revises: 26db9a676175
Create Date: 2020-01-03 13:32:02.565935

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '743d6ef273d1'
down_revision = '26db9a676175'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cities', sa.Column('image', sa.String(length=100), nullable=True))
    op.drop_column('cities', 'description')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cities', sa.Column('description', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    op.drop_column('cities', 'image')
    # ### end Alembic commands ###
