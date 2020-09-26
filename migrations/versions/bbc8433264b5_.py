"""empty message

Revision ID: bbc8433264b5
Revises: 72b684813fd7
Create Date: 2020-06-16 20:46:47.737957

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bbc8433264b5'
down_revision = '72b684813fd7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('gametypes',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('games',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('type_id', sa.Integer(), nullable=False),
    sa.Column('running', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['type_id'], ['gametypes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('players',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('creator_id', sa.Integer(), nullable=True),
    sa.Column('game_id', sa.Integer(), nullable=False),
    sa.Column('deployment_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['creator_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['deployment_id'], ['deployments.id'], ),
    sa.ForeignKeyConstraint(['game_id'], ['games.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('players')
    op.drop_table('games')
    op.drop_table('gametypes')
    # ### end Alembic commands ###
