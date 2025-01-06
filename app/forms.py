from wtforms import SelectField, StringField, SubmitField, PasswordField, IntegerField, HiddenField, BooleanField, DecimalField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

class AddExerciseForm(FlaskForm):
    name = StringField("Exercise Name", validators=[DataRequired()])
    muscle_group = SelectField("Muscle Group", coerce=int)
    weighted = BooleanField("Weighted")
    weight = DecimalField("Weight", places=2, default=0)
    submit = SubmitField("Add Exercise")

class UpdateExerciseForm(FlaskForm):
    id = HiddenField("ID")
    name = StringField("Exercise Name", validators=[DataRequired()])
    muscle_group = SelectField("Muscle Group", coerce=int)
    weighted = BooleanField("Weighted")
    weight = DecimalField("Weight", places=2)
    submit = SubmitField("Update Exercise")
    rep_pr = IntegerField("PR", default=0)

    #Ensure correct default muscle group is selected
    def __init__(self, muscle_group=None, *args, **kwargs):
        super(UpdateExerciseForm, self).__init__(*args, **kwargs)
        if muscle_group:
            self.muscle_group.default = muscle_group
            self.process()

class AddWorkoutForm(FlaskForm):
    name = StringField("Workout Name", validators=[DataRequired()])
