from app import db
from datetime import datetime
import random

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

# Association table for Workout and Exercise (current routine)
workout_current_routine = db.Table('workout_current_routine',
    db.Column('workout_id', db.Integer, db.ForeignKey('workout.id'), primary_key=True),
    db.Column('exercise_id', db.Integer, db.ForeignKey('exercise.id'), primary_key=True)
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
    time = db.Column(db.DateTime, default=db.func.current_timestamp())
    current_routine = db.relationship('Exercise', secondary=workout_current_routine, lazy='subquery',
                                      backref=db.backref('current_workouts', lazy=True))
    
    def generate_routine(self):
        order = self.order
        exercises = self.exercises
        groups = self.muscle_groups
        workout_time = self.time
        print(self.name, order, exercises, groups)

        current_time = datetime.now()
        if (current_time.date() > workout_time.date()) or (not self.current_routine):
            chosen_groups = {}
            generated_exercises = []
            for i in groups:
                chosen_groups[i.id] = [x for x in Exercise.query.filter_by(muscle_group_id=i.id).all()]
            for i in order:
                if i == '0':
                    generated_exercises.append(chosen_groups[groups[0].id].pop(random.randint(0, len(chosen_groups[groups[0].id])-1)))
                    groups.pop(0)
                else:
                    generated_exercises.append(exercises.pop(0))
            print(generated_exercises)
            self.current_routine = generated_exercises
            self.time = current_time
            db.session.commit()
            return generated_exercises
        else: return self.current_routine