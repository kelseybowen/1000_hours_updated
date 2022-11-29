from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models import users
from flask_app.models import logs 
from flask_app.controllers import logs_controller
from datetime import datetime
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/register', methods=["POST"])
def register():
    if not users.User.validate_registration(request.form):
        session['first_name'] = request.form['first_name']
        session['last_name'] = request.form['last_name']
        session['email'] = request.form['r_email']
        return redirect('/')
    data = {
        "first_name": request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["r_email"],
        "password": bcrypt.generate_password_hash(request.form["r_password"])
    }
    user_id = users.User.save_user(data)
    session['user_id'] = user_id
    session['first_name'] = data["first_name"]
    return redirect('/dashboard')

    
@app.route('/login', methods=["POST"])
def login():
    user_in_db = users.User.get_user_by_email(request.form["l_email"])
    if not user_in_db:
        flash("Invalid Email", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['l_password']):
        flash("Invalid Password", 'login')
        return redirect('/')
    session['user_id'] = user_in_db.id
    session['first_name'] = user_in_db.first_name
    session['last_name'] = user_in_db.last_name
    return redirect('/dashboard')


@app.route('/dashboard')
def show_dashboard():
    user_info = users.User.get_user_info(session['user_id'])
    user_logs = logs.Log.get_all_user_logs(session['user_id'])
    return render_template("dashboard.html", user_info=user_info, user_logs=user_logs)

@app.route('/edit_user/<int:id>')
def edit_user_goal(id):
    user_info = users.User.get_user_info(id)
    return render_template("edit_user.html", user_info=user_info)

@app.route('/update_user/<int:id>', methods=["POST"])
def update_user_goal(id):
    data = {
        "goal_hours": request.form["goal_hours"],
        "id": id
    }
    users.User.update_user_goal(data)
    return redirect('/dashboard')

@app.route('/create_log', methods=["POST"])
def create_log():
    data = {
        "date": request.form["date"],
        "minutes": request.form["minutes"],
        "user_id": session["user_id"]
    }
    logs.Log.create_log(data)
    return


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
