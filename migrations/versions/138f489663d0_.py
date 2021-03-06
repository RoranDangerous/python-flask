"""empty message

Revision ID: 138f489663d0
Revises: b4a9c0be3623
Create Date: 2020-06-09 19:45:38.530478

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '138f489663d0'
down_revision = 'b4a9c0be3623'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('kubecontainers', sa.Column('options', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    op.drop_column('kubecontainers', 'username')
    op.drop_column('kubecontainers', 'password')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('kubecontainers', sa.Column('password', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('kubecontainers', sa.Column('username', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.drop_column('kubecontainers', 'options')
    # ### end Alembic commands ###
