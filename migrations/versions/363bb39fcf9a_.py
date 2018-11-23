"""empty message

Revision ID: 363bb39fcf9a
Revises: 840a241a5ad3
Create Date: 2018-11-14 18:54:58.865500

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '363bb39fcf9a'
down_revision = '840a241a5ad3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('UserId', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=16), nullable=True),
    sa.Column('password', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('UserId')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
