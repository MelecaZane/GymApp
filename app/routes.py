from flask import render_template, request, redirect, url_for, flash, jsonify
from app import flask_app
from app import db
from app.models import MuscleGroup, Exercise, Workout
from app.forms import AddExerciseForm, UpdateExerciseForm, AddWorkoutForm
from werkzeug.datastructures import MultiDict
import random
from datetime import datetime

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
            print(form.weighted.data)
            if form.weighted.data:
                new_exercise = Exercise(name=form.name.data,
                                        muscle_group_id=form.muscle_group.data,
                                        weighted=form.weighted.data,
                                        weight=form.weight.data)
            else:
                new_exercise = Exercise(name=form.name.data,
                                        muscle_group_id=form.muscle_group.data,
                                        weighted=form.weighted.data,
                                        weight=0)
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

@flask_app.route('/exerciseDetails/<int:exercise_id>', methods=["GET", "POST"])
def exercise_details_page(exercise_id):
    exercise = Exercise.query.get(exercise_id)
    form = UpdateExerciseForm(obj=exercise, muscle_group=exercise.muscle_group_id)

    muscle_groups = MuscleGroup.query.all()
    form.muscle_group.choices = [(muscle_group.id, muscle_group.name) for muscle_group in muscle_groups]

    if request.method == "GET":
        return render_template("exerciseDetails.html",
                                title=f"{exercise.name} Details",
                                exercise=exercise,
                                form=form)

    if request.method == "POST":
        if form.validate_on_submit():
            exercise.name = form.name.data
            exercise.muscle_group_id = form.muscle_group.data
            exercise.weighted = form.weighted.data
            exercise.weight = form.weight.data
            exercise.rep_pr = form.rep_pr.data

            db.session.commit()
            flash("Exercise added!")
            print("ADDED EXERCISE")
            return redirect(url_for("all_exercises_page"))
        else:
            flash("Error adding exercise!")
            print("ERROR ADDING EXERCISE")
            print(form.errors)
            return redirect(url_for("all_exercises_page"))
        
@flask_app.route("/allWorkouts", methods=["GET"])
def all_workouts_page():
    workouts = Workout.query.all()
    return render_template("allWorkouts.html",
                            title="All Workouts",
                            workouts=workouts)

@flask_app.route("/addWorkout", methods=["GET", "POST"])
def add_workout_page():
    if request.method == "GET":
        exercises = Exercise.query.all()
        exercise_choices = [(exercise.id, exercise.name) for exercise in exercises]
        muscle_groups = MuscleGroup.query.all()
        muscle_group_choices = [(muscle_group.id, muscle_group.name) for muscle_group in muscle_groups]

        return render_template("addWorkout.html",
                                title="Add Workout",
                                exercises=exercise_choices,
                                muscle_groups=muscle_group_choices,
                                form=AddWorkoutForm())
    
    if request.method == "POST":
        workout_details = request.json
        order = workout_details["order"]
        order = [str(x) for x in order]
        print(workout_details["exercises"])
        print(workout_details["groups"])
        exercises = [Exercise.query.get(x) for x in workout_details["exercises"]]
        groups = [MuscleGroup.query.get(x) for x in workout_details["groups"]]
        print(exercises)
        print(groups)

        new_workout = Workout(name=workout_details["name"],
                                exercises=exercises,
                                muscle_groups=groups,
                                order=''.join(order))
        db.session.add(new_workout)
        db.session.commit()
        return jsonify({"success": True, "redirect_url": url_for('all_workouts_page')}), 200

@flask_app.route("/workoutDetails/<int:workout_id>", methods=["GET", "POST"])
def view_workout_page(workout_id):
    if request.method == "GET":
        workout = Workout.query.get(workout_id)
        generated_exercises = workout.generate_routine()

        return render_template("viewWorkout.html",
                            title=workout.name,
                            exercises=generated_exercises,
                            form=UpdateExerciseForm(),
                            workout_id=workout_id)
    
    if request.method == "POST":
        update_details = request.json
        exercise = Exercise.query.get(update_details["id"])
        if exercise.weighted:
            exercise.weight = update_details["data"]
        else:
            exercise.rep_pr = update_details["data"]
        db.session.commit()
        return jsonify({"success": True, "redirect_url": url_for('view_workout_page', workout_id=update_details["workout"])}), 200