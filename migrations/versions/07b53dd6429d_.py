"""empty message

Revision ID: 07b53dd6429d
Revises: 4eb7046f053d
Create Date: 2018-11-19 11:34:53.101744

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '07b53dd6429d'
down_revision = '4eb7046f053d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Colors', 'ColorSet',
               existing_type=mysql.INTEGER(display_width=11),
               type_=sa.Enum('Item', 'Hair', 'Skin', name='colorset'),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Colors', 'ColorSet',
               existing_type=sa.Enum('Item', 'Hair', 'Skin', name='colorset'),
               type_=mysql.INTEGER(display_width=11),
               existing_nullable=False)
    # ### end Alembic commands ###
