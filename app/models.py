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