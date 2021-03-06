"""empty message

Revision ID: b6bc2c6074a3
Revises: 2f505d1e22ad
Create Date: 2020-09-25 08:39:24.972218

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from datetime import datetime
# revision identifiers, used by Alembic.
revision = 'b6bc2c6074a3'
down_revision = '2f505d1e22ad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('comments', 'date',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('comments', 'date',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=True)
    # ### end Alembic commands ###
