from app import app, forms, db, login_manager
from flask import render_template, url_for, redirect
from app.models import habits, users


@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    Habits=habits.query.all()
    form=forms.HabitCheck()
    return render_template('dashboard.html', Habits=Habits, form=form)

@app.route('/addhabit', methods=['get','post'])
def addhabit():
    form=forms.HabitForm()
    if form.validate_on_submit():
        NewHabit=habits(name=form.name.data)
        db.session.add(NewHabit)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('addHabit.html', form=form)

@app.route('/login', methods=['get','post'])
def login():
    form=forms.LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('dashboard'))
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