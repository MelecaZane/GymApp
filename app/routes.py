from flask import render_template, request, redirect, url_for, flash
from app import flask_app
from app import db

@flask_app.route("/", methods=["GET", "POST"])
@flask_app.route("/index.html", methods=["GET", "POST"])
@flask_app.route("/home", methods=["GET", "POST"])
def home_page():
    return "Hello, World!"