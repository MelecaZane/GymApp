"""empty message

Revision ID: dacfa9cdd3b6
Revises: fd90bb4e3817
Create Date: 2025-01-06 11:14:50.402115

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dacfa9cdd3b6'
down_revision = 'fd90bb4e3817'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('workout',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('workout', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_workout_name'), ['name'], unique=True)

    op.create_table('workout_muscle_groups',
    sa.Column('workout_id', sa.Integer(), nullable=False),
    sa.Column('muscle_group_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['muscle_group_id'], ['muscle_group.id'], ),
    sa.ForeignKeyConstraint(['workout_id'], ['workout.id'], ),
    sa.PrimaryKeyConstraint('workout_id', 'muscle_group_id')
    )
    op.create_table('workout_exercises',
    sa.Column('workout_id', sa.Integer(), nullable=False),
    sa.Column('exercise_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['exercise_id'], ['exercise.id'], ),
    sa.ForeignKeyConstraint(['workout_id'], ['workout.id'], ),
    sa.PrimaryKeyConstraint('workout_id', 'exercise_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('workout_exercises')
    op.drop_table('workout_muscle_groups')
    with op.batch_alter_table('workout', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_workout_name'))

    op.drop_table('workout')
    # ### end Alembic commands ###
