"""remove password_confirm column for users tables

Revision ID: 4d96808c1a1f
Revises: c963943a27fb
Create Date: 2023-11-23 02:57:21.496205

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4d96808c1a1f'
down_revision = 'c963943a27fb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('password_confirm')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password_confirm', mysql.VARCHAR(length=255), nullable=False))

    # ### end Alembic commands ###
