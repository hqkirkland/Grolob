"""empty message

Revision ID: 8041f33acc52
Revises: 
Create Date: 2018-12-16 18:09:32.141827

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8041f33acc52'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('GameItem', sa.Column('Layered', sa.Enum('T', 'F', name='singleenum'), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('GameItem', 'Layered')
    # ### end Alembic commands ###
