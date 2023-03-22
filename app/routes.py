from app import app, forms, db, login_manager
from flask import render_template, url_for, redirect, flash
from app.models import habits, users
from flask_login import login_required, current_user,logout_user, login_user
from werkzeug.security import check_password_hash
@login_manager.user_loader
def load_user(user_id):
    return users.query.get(user_id)


@app.route('/', methods=['get','post'])
def index():
    return render_template('index.html')

@login_required
@app.route('/dashboard')
def dashboard():
    Habits=habits.query.all()
    form=forms.HabitCheck()
    return render_template('dashboard.html', Habits=Habits, form=form)


@login_required
@app.route('/addhabit', methods=['get','post'])
def addhabit():
    form=forms.HabitForm()
    if form.validate_on_submit():
        NewHabit=habits(name=form.name.data, userid=current_user.id)
        db.session.add(NewHabit)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('addHabit.html', form=form)

@app.route('/login', methods=['get','post'])
def login():
    form=forms.LoginForm()
    if form.validate_on_submit():
        user=users.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password_hash,form.password.data):
                login_user(user)
                flash("Login Succeesful")
                print(current_user.id)
                return redirect(url_for('dashboard'))
            else:
                flash("Wrong password")
        else:
            flash("User doesn't exist")
    return render_template('login.html', form=form)


@app.route('/register', methods=['get', 'post'])
def register():
    form=forms.RegisterForm()
    if form.validate_on_submit():
     newuser = users(username=form.username.data, email=form.email.data)
     newuser.set_password(form.password1.data)
     print(newuser)
     db.session.add(newuser)
     db.session.commit()
     return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/logout', methods=['get'])
@login_required
def logut():
    logout_user()
    return redirect(url_for('index'))