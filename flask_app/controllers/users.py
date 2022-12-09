from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User


@app.route("/")
def login_page():
    #we will come back and add (IF IN SESSION)
    return render_template("login.html")

@app.route("/register", methods=['POST'])
def register():

    user = User.validate_register(request.form)

    if not user:
        return redirect("/")

    session['user_id'] = user

    return redirect("/recipes")


@app.route("/login", methods=['POST'])
def login():
    user = User.validate_login(request.form)

    if not user:
        return redirect("/")

    session["user_id"] = user.id
    session["user_name"] = user.first_name

    return redirect("/recipes")

@app.route("/logout")
def logout():
    session.clear()

    return redirect("/")