from app import app, forms, db, login_manager
from flask import render_template, url_for, redirect, flash, request
from app.models import habits, users, streak
from flask_login import login_required, current_user,logout_user, login_user
from werkzeug.security import check_password_hash
from sqlalchemy.exc import IntegrityError

"""
All routes related to managing user activity
Userloader to intialize flask_login and current user. 

The Login route is for already registered users to login into there accounts. Checks if user exists and if they exist checks if password is correct. 
Else will false message to alert user. 
If user is already logged in they will be redirected to the info page. 

The Register route is for new user to sign up and create accounts. 
Checks to see if any of the credentials that the user has put in are already taken or not valid and then flash them to the user incase they are as well as not allowing it in the database to prevent errors. 

The logout route logouts users using flask_login so multiple users can log onto the same computer without having to use the same account. 

"""

@login_manager.user_loader
def load_user(user_id):
    return users.query.get(user_id)

@app.route('/login', methods=['get','post'])
def login():
    form=forms.LoginForm()
    if current_user.is_authenticated:
        flash("Your already logged in silly :)")
        return redirect(url_for('info'))
    if form.validate_on_submit():
        user=users.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password_hash,form.password.data):
                login_user(user)
                flash("Login Succeesful")
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
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/', methods=['get','post'])
def index():
    return render_template('index.html')



@app.route('/addhabit', methods=['GET', 'POST'])
@login_required
def addhabit():
    form = forms.HabitForm()
    if form.validate_on_submit():
        checkhabit=habits.query.filter_by(user_id=current_user.id, name=form.name.data.title()).first()
        if checkhabit:
            flash('You already have this habit')
            return redirect(url_for('addhabit'))
        else:
            NewHabit = habits(name=form.name.data.title(), reason=form.reason.data.title(),user_id=current_user.id)
            db.session.add(NewHabit)
            db.session.commit()
            flash('Habit added successfully!', 'success')
            return redirect(url_for('dashboard'))
    return render_template('addHabit.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    Habits=habits.query.filter_by(user_id=current_user.id)
    form=forms.YesNo()
    return render_template('dashboard.html', Habits=Habits, form=form)

@app.route('/streaks')
@login_required
def streaks():
    Streaks=streak.query.filter_by(user_id=current_user.id)
    print(Streaks)
    return render_template('streak.html', Streaks=Streaks)


@app.route('/info')
def info():
    if current_user.is_authenticated:
        form=forms.YesNo()
        return render_template('info.html', form=form)
    else:
        flash("You haven't logged on you can't access this page")
        return redirect(url_for('login'))


@app.route('/faq', methods=['get'])
def faq():
    faqs = {
    "What is this app about?": "Hadit is a habit tracker meant to help neurodivergent people as well as thoose with psychological conditions. By offering a customizable and more engaging way for people to achieve there habits",
    "How do I create an account?": "Go onto signup page. Enter your email, username, password. And then do recaptcha to make sure your not a robot. Afterwards if all your details are valid you should be logged in.",
    "How do I add a new habit?": "First sign into your account or create a new account. Afterwards navigate to add habit route and enter the details or your habit and optionally enter the reason you want to do your habit.",
    "How do I check off a completed habit?": "Make sure you are signed into your account. Navigate to dashboard and then select the checkbox if you have done your habit.",
    "Can I use this app on multiple devices?": "Yes, Hadit is a website created using Flask, HTML, CSS, and Javascript. And is capable of running on any modern webbrowser without any need for any special configuration. Just sign into your account and your informaton should sync from you account seamlessly. ",
    "Is my personal information secure on this app?": "Yes. Hadit hashes all the passwords from users as well as encrypting any text entered for the reason user input for habits. To try to ensure users privacy.",
    "What happens if I encounter an error or bug?": "If a red message occurs this may be a sign that you might need to check your input to see if there are any errors. This could be from entering a duplicate habit, the incorrect password, or a username that doesn't exist. Else users would be redirected to a error page where you can be taken back to the website afterwards. ",
    "What types of customizability do you current offer": "Currently Hadit offers the ability to change from Light to Dark mode in the user info page. As well there is a page for cats incase you want to look at some adorable cutie pies. "
}
    return render_template('faq.html', faqs=faqs)


@app.route('/cats', methods=['get'])
def cats():
    return render_template('cats.html')


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
    return render_template('error.html', error_code=406, error_description='Method Not Allowed', error_message='Sorry, the method you used to access this page is not allowed.'), 405

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
