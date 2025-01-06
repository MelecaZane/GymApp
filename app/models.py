from app import db

class MuscleGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    exercises = db.relationship("Exercise", backref="muscle_group", lazy="dynamic")

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    weighted = db.Column(db.Boolean, default=True)
    weight = db.Column(db.Float, default=0)
    rep_pr = db.Column(db.Integer, default=0)
    muscle_group_id = db.Column(db.Integer, db.ForeignKey("muscle_group.id"))

# Association table for Workout and Exercise
workout_exercises = db.Table('workout_exercises',
    db.Column('workout_id', db.Integer, db.ForeignKey('workout.id'), primary_key=True),
    db.Column('exercise_id', db.Integer, db.ForeignKey('exercise.id'), primary_key=True)
)

# Association table for Workout and MuscleGroup
workout_muscle_groups = db.Table('workout_muscle_groups',
    db.Column('workout_id', db.Integer, db.ForeignKey('workout.id'), primary_key=True),
    db.Column('muscle_group_id', db.Integer, db.ForeignKey('muscle_group.id'), primary_key=True)
)

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    order = db.Column(db.String, default='')
    #0
    muscle_groups = db.relationship('MuscleGroup', secondary=workout_muscle_groups, lazy='subquery',
                                    backref=db.backref('workouts', lazy=True))
    #1
    exercises = db.relationship('Exercise', secondary=workout_exercises, lazy='subquery',
                                backref=db.backref('workouts', lazy=True))