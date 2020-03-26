"""empty message

Revision ID: d1730ee4064c
Revises: 2e121a79696e
Create Date: 2020-03-26 20:46:56.061060

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd1730ee4064c'
down_revision = '2e121a79696e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('location',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('addres', sa.String(length=1024), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('items', sa.Column('created', sa.DateTime(), server_default='2020-03-26 19:46:55.987148', nullable=False))
    op.add_column('items', sa.Column('updated', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('created', sa.DateTime(), server_default='2020-03-26 19:46:55.987148', nullable=False))
    op.add_column('users', sa.Column('updated', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'updated')
    op.drop_column('users', 'created')
    op.drop_column('items', 'updated')
    op.drop_column('items', 'created')
    op.drop_table('location')
    # ### end Alembic commands ###
