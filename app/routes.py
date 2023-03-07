from app import app, forms, db
from flask import render_template, url_for, redirect
from app.models import habits

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    Habits=habits.query.all()
    return render_template('dashboard.html', Habits=Habits)

@app.route('/addhabit', methods=['get','post'])
def addhabit():
    form=forms.habitform()
    if form.validate_on_submit():
        NewHabit=habits(name=form.name.data)
        db.session.add(NewHabit)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('addHabit.html', form=form)

@app.route('/login', methods=['get','post'])
def login():
    return render_template('login.html')