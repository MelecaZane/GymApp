from wtforms import SelectField, StringField, SubmitField, PasswordField, IntegerField, HiddenField, BooleanField, DecimalField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

class AddExerciseForm(FlaskForm):
    name = StringField("Exercise Name", validators=[DataRequired()])
    muscle_group = SelectField("Muscle Group", coerce=int)
    weighted = BooleanField("Weighted")
    weight = DecimalField("Weight", places=2)
    submit = SubmitField("Add Exercise")