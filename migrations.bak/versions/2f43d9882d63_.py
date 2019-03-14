"""empty message

Revision ID: 2f43d9882d63
Revises: 478850928c03
Create Date: 2019-03-13 22:06:57.558285

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f43d9882d63'
down_revision = '478850928c03'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'trackrate', ['rate_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'trackrate', type_='unique')
    # ### end Alembic commands ###
