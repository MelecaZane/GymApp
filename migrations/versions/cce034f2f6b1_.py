"""empty message

Revision ID: cce034f2f6b1
Revises: 
Create Date: 2025-01-02 15:43:23.832959

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cce034f2f6b1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('exercise',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('weighted', sa.Boolean(), nullable=True),
    sa.Column('weight', sa.Float(), nullable=True),
    sa.Column('rep_pr', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('exercise', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_exercise_name'), ['name'], unique=True)

    op.create_table('muscle_group',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('muscle_group', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_muscle_group_name'), ['name'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('muscle_group', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_muscle_group_name'))

    op.drop_table('muscle_group')
    with op.batch_alter_table('exercise', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_exercise_name'))

    op.drop_table('exercise')
    # ### end Alembic commands ###
