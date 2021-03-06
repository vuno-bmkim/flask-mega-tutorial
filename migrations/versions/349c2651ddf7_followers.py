"""followers

Revision ID: 349c2651ddf7
Revises: 37fb0784c307
Create Date: 2019-02-19 14:57:32.608400

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '349c2651ddf7'
down_revision = '37fb0784c307'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('followers')
    # ### end Alembic commands ###
