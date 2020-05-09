"""empty message

Revision ID: 868c3d62e224
Revises: e4bf0705b23e
Create Date: 2020-05-07 06:08:21.743078

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '868c3d62e224'
down_revision = 'e4bf0705b23e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('todo_lists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('todos', sa.Column('list_id', sa.Integer(), nullable=True))
    op.alter_column('todos', 'completed',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.create_foreign_key(None, 'todos', 'todo_lists', ['list_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'todos', type_='foreignkey')
    op.alter_column('todos', 'completed',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.drop_column('todos', 'list_id')
    op.drop_table('todo_lists')
    # ### end Alembic commands ###