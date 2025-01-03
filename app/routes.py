from flask import render_template, request, redirect, url_for, flash
from app import flask_app
from app import db
from app.models import MuscleGroup, Exercise
from app.forms import AddExerciseForm

@flask_app.route("/", methods=["GET", "POST"])
@flask_app.route("/index.html", methods=["GET", "POST"])
@flask_app.route("/home", methods=["GET", "POST"])
def home_page():
    return render_template("index.html",
                            title="Home")

@flask_app.route("/addExercises", methods=["GET", "POST"])
def add_exercise_page():
    form = AddExerciseForm()

    muscle_groups = MuscleGroup.query.all()
    form.muscle_group.choices = [(muscle_group.id, muscle_group.name) for muscle_group in muscle_groups]
    if request.method == "GET":
        return render_template("addExercises.html",
                                title="Add Exercise",
                                form=form)
    if request.method == "POST":
        if form.validate_on_submit():
            new_exercise = Exercise(name=form.name.data,
                                    muscle_group_id=form.muscle_group.data,
                                    weighted=form.weighted.data,
                                    weight=form.weight.data)
            db.session.add(new_exercise)
            db.session.commit()
            flash("Exercise added!")
            print("ADDED EXERCISE")
            return redirect(url_for("add_exercise_page"))
        else:
            flash("Error adding exercise!")
            print("ERROR ADDING EXERCISE")
            return redirect(url_for("add_exercise_page"))
        
@flask_app.route("/allExercises", methods=["GET", "POST"])
def all_exercises_page():
    muscle_groups = MuscleGroup.query.all()
    exercises = {}
    for muscle_group in muscle_groups:
        exercises[muscle_group.name] = Exercise.query.filter_by(muscle_group_id=muscle_group.id).all()
    return render_template("allExercises.html",
                    title="All Exercises",
                    exercises=exercises)