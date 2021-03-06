"""empty message

Revision ID: 9224cd4fb624
Revises: 8451b27fa1b6
Create Date: 2020-04-24 14:53:50.229983

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9224cd4fb624'
down_revision = '8451b27fa1b6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('deployments',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('deployments')
    # ### end Alembic commands ###
