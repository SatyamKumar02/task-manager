from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import login_manager, db
from app.models import User
from app.forms import SignupForm, LoginForm
from app.models import Task
from app.forms import TaskForm
from bson.objectid import ObjectId


main = Blueprint('main', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(db, user_id)

@main.route("/")
def home():
    return redirect(url_for("main.login"))

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        existing_user = db.users.find_one({'email': form.email.data})
        if existing_user:
            flash('Email already registered.')
            return redirect(url_for('main.signup'))
        user = User.create(db, form.username.data, form.email.data, form.password.data)
        login_user(user)
        flash('Account created and logged in!')
        return redirect(url_for('main.dashboard'))
    return render_template('signup.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(db, form.email.data)
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid email or password.')
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.login'))

@main.route('/task/add', methods=['GET', 'POST'])
@login_required
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        Task.create(
            db,
            current_user.id,
            form.title.data,
            form.description.data,
            form.category.data,
            form.due_date.data
        )
        flash('Task added.')
        return redirect(url_for('main.dashboard'))
    return render_template('task_form.html', form=form)

@main.route('/task/edit/<task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.get_by_id(db, task_id)
    if task['user_id'] != ObjectId(current_user.id):
        flash("Unauthorized.")
        return redirect(url_for('main.dashboard'))

    form = TaskForm(data=task)
    if form.validate_on_submit():
        updates = {
            'title': form.title.data,
            'description': form.description.data,
            'category': form.category.data,
            'due_date': form.due_date.data
        }
        Task.update(db, task_id, updates)
        flash('Task updated.')
        return redirect(url_for('main.dashboard'))

    return render_template('task_form.html', form=form, editing=True)

@main.route('/task/delete/<task_id>')
@login_required
def delete_task(task_id):
    Task.delete(db, task_id)
    flash('Task deleted.')
    return redirect(url_for('main.dashboard'))

@main.route('/task/toggle/<task_id>')
@login_required
def toggle_task(task_id):
    Task.toggle_complete(db, task_id)
    flash('Task updated.')
    return redirect(url_for('main.dashboard'))

@main.route('/dashboard')
@login_required
def dashboard():
    tasks = Task.get_by_user(db, current_user.id)
    return render_template('dashboard.html', tasks=tasks)