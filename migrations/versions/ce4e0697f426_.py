"""empty message

Revision ID: ce4e0697f426
Revises: 2de6f7197b73
Create Date: 2024-08-07 19:18:38.025371

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ce4e0697f426'
down_revision = '2de6f7197b73'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('builds', schema=None) as batch_op:
        batch_op.add_column(sa.Column('author_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('author_id', 'users', ['author_id'], ['id'])

    with op.batch_alter_table('builds', schema=None) as batch_op:
        op.execute('UPDATE builds SET author_id = 1')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('builds', schema=None) as batch_op:
        batch_op.drop_constraint('author_id', type_='foreignkey')
        batch_op.drop_column('author_id')

    # ### end Alembic commands ###