"""empty message

Revision ID: 69e1490c3e0c
Revises: 38f8308da074
Create Date: 2017-09-12 18:44:13.025704

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '69e1490c3e0c'
down_revision = '38f8308da074'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('admin', sa.Boolean(), nullable=True))
    op.drop_column('users', 'is_admin')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_admin', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('users', 'admin')
    # ### end Alembic commands ###
