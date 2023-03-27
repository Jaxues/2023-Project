from app import app, forms, db, login_manager
from flask import render_template, url_for, redirect, flash, request
from app.models import habits, users
from flask_login import login_required, current_user,logout_user, login_user
from werkzeug.security import check_password_hash
from sqlalchemy.exc import IntegrityError
@login_manager.user_loader
def load_user(user_id):
    return users.query.get(user_id)


@app.route('/', methods=['get','post'])
def index():
    return render_template('index.html')


@app.route('/dashboard')
@login_required
def dashboard():
    Habits=habits.query.all()
    form=forms.HabitCheck()
    return render_template('dashboard.html', Habits=Habits, form=form)



@app.route('/addhabit', methods=['get','post'])
@login_required
def addhabit():
    form=forms.HabitForm()
    if form.validate_on_submit():
        NewHabit=habits(name=form.name.data, userid=current_user.id)
        db.session.add(NewHabit)
        db.session.commit()
        flash('Habit added to database')
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
        try:
            db.session.commit()
            return redirect(url_for('login'))
        except IntegrityError:
            db.session.rollback()
            flash('User already exists')
    return render_template('register.html', form=form)


@app.route('/logout', methods=['get'])
@login_required
def logut():
    logout_user()
    return redirect(url_for('index'))

@app.errorhandler(400)
def bad_request(error):
    return render_template('error.html', error_code=400, error_description='Bad Request', error_message='Sorry, there was a problem with your request.'), 400

@app.errorhandler(401)
def unauthorized(error):
    return render_template('error.html', error_code=401, error_description='Unauthorized', error_message='Sorry, you don\'t have access to this page.'), 401

@app.errorhandler(403)
def forbidden(error):
    return render_template('error.html', error_code=403, error_description='Forbidden', error_message='Sorry, you don\'t have permission to access this page.'), 403

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error_code=404, error_description='Page Not Found', error_message='Sorry, we couldn\'t find the page you were looking for.'), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return render_template('error.html', error_code=405, error_description='Method Not Allowed', error_message='Sorry, the method you used to access this page is not allowed.'), 405

@app.errorhandler(500)
def internal_server_error(error):
    db.session.rollback()
    return render_template('error.html', error_code=500, error_description='Internal Server Error', error_message='Sorry, there was an internal server error.'), 500

@app.errorhandler(IntegrityError)
def handle_integrity_error(error):
    db.session.rollback()
    flash('Integrity error occurred')
    return redirect(url_for('register'))

@app.errorhandler(Exception)
def handle_all_other_errors(error):
    db.session.rollback()
    flash('An error occurred')
    return render_template('error.html', error_code=500, error_description='Internal Server Error', error_message='Sorry, there was an internal server error.'), 500
