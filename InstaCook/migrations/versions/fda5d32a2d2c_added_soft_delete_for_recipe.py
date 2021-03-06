"""Added soft delete for recipe

Revision ID: fda5d32a2d2c
Revises: 35cf2e08ab31
Create Date: 2021-11-27 11:44:14.223728

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fda5d32a2d2c'
down_revision = '35cf2e08ab31'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('recipe', sa.Column('is_deleted', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('recipe', 'is_deleted')
    # ### end Alembic commands ###
