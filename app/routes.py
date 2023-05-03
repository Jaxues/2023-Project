from app import app, forms, db, login_manager
from flask import render_template, url_for, redirect, flash, jsonify, request
from app.models import habits, users, streak
from flask_login import login_required, current_user, logout_user, login_user
from werkzeug.security import check_password_hash
from sqlalchemy.exc import IntegrityError



@login_manager.user_loader 
# Define userloader to Users ID
def load_user(user_id): 
    # Create function 
    return users.query.get(user_id) # Returns current users_id from 'users' table


@app.route("/login", methods=["get", "post"]) 
# define login route
def login(): 
    # Create login function 
    form = forms.LoginForm() 
    # Set form variable to be equal to Loginform class from forms.py
    if current_user.is_authenticated:   
        # If current users is already logged in flash message
        flash("Your already logged in silly :)")
        return redirect(url_for("info"))
    if form.validate_on_submit(): 
        # Once user has submited form check with logic
        user = users.query.filter_by(username=form.username.data).first() 
        # See if user exists
        if user: 
            # If user exists continue
            if check_password_hash(user.password_hash, form.password.data): 
                # See if entered password from user is same as stored hashed password
                login_user(user) 
                # If successful log in user
                flash("Login Succeesful") 
                # Alert user that proccess was succesful
                return redirect(url_for("dashboard")) 
            # Return to page where user can see most recent habits
            else:
                flash("Wrong password")
                # If user entered password is incorrect. Won't log in user
        else:
            flash("User doesn't exist") 
            # If user isn't created alert user
    return render_template("login.html", form=form)


@app.route("/register", methods=["get", "post"]) 
# Define register route
def register():
    form = forms.RegisterForm()
    # Set form variable to be equal to RegisterForm class from forms.py
    if form.validate_on_submit():
        # Once user has succesfully submited form
        newuser = users(username=form.username.data, email=form.email.data)
        # set newuser variable to be equal to have username and email to same as entered credentials
        newuser.set_password(form.password1.data) 
        # Set password hash for new user
        print(newuser)
        # Validate that newuser is created correctly
        db.session.add(newuser)

        """
        
        Try to add newuser to database and if succesful add them to database

        If user already exists rollback database and alert user
        
        """


        try:
            db.session.commit()
            return redirect(url_for("login"))
        except IntegrityError:
            db.session.rollback()
            flash("User already exists")
    return render_template("register.html", form=form)


"""

Define logout function for user
Loginrequired as program can't logout users who aren't authenticated
Once routed will logout user from session and then return them to index page

"""

@app.route("/logout", methods=["get"]) 
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/", methods=["get", "post"])
def index():
    return render_template("index.html")


@app.route("/addhabit", methods=["GET", "POST"])
@login_required
def addhabit():
    form = forms.HabitForm()
    if form.validate_on_submit():
        checkhabit = habits.query.filter_by(
            user_id=current_user.id, name=form.name.data.title()
        ).first()
        print('Habit Added')
        if checkhabit:
            flash("You already have this habit")
            return redirect(url_for("addhabit"))
        else:
            NewHabit = habits(
                name=form.name.data.title(),
                reason=form.reason.data.title(),
                user_id=current_user.id,
            )
            db.session.add(NewHabit)
            db.session.commit()
            flash("Habit added successfully!", "success")
            return redirect(url_for("dashboard"))
    return render_template("addHabit.html", form=form)


@app.route("/dashboard", methods=['GET','POST'])
@login_required
def dashboard():
    Habits = habits.query.filter_by(user_id=current_user.id)
    form = forms.StreakForm()
    if form.validate_on_submit():
        new_entry=streak(user_id=current_user.id, habit_id=form.hidden_id.data)
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('streaks'))
    return render_template("dashboard.html", Habits=Habits, form=form)



@app.route("/streaks", methods=['get', 'post'])
@login_required
def streaks():
    Streaks = streak.query.filter_by(user_id=current_user.id)
    return render_template("streak.html", Streaks=Streaks)

@app.route("/info")
def info():
    if current_user.is_authenticated:
        form = forms.YesNo()
        return render_template("info.html", form=form)
    else:
        flash("You haven't logged on you can't access this page")
        return redirect(url_for("login"))

# Email perferences to subscribe user to email
@app.route("/subscribe", methods=['get', 'post'])
@login_required
def subscribe():
    email_user=users.query.filter_by(id=current_user.id).first()
    email_user.email_notifactions=True
    db.session.add(email_user)
    db.session.commit()
    flash('Email perferences updated')
    return redirect(url_for('info'))

@app.route("/faq", methods=["get"])
def faq():
    faqs = {
        "What is this app about?": "Hadit is a habit tracker meant to help neurodivergent people as well as thoose with psychological conditions. By offering a customizable and more engaging way for people to achieve there habits",
        "How do I create an account?": "Go onto signup page. Enter your email, username, password. And then do recaptcha to make sure your not a robot. Afterwards if all your details are valid you should be logged in.",
        "How do I add a new habit?": "First sign into your account or create a new account. Afterwards navigate to add habit route and enter the details or your habit and optionally enter the reason you want to do your habit.",
        "How do I check off a completed habit?": "Make sure you are signed into your account. Navigate to dashboard and then select the checkbox if you have done your habit.",
        "Can I use this app on multiple devices?": "Yes, Hadit is a website created using Flask, HTML, CSS, and Javascript. And is capable of running on any modern webbrowser without any need for any special configuration. Just sign into your account and your informaton should sync from you account seamlessly. ",
        "Is my personal information secure on this app?": "Yes. Hadit hashes all the passwords from users as well as encrypting any text entered for the reason user input for habits. To try to ensure users privacy.",
        "What happens if I encounter an error or bug?": "If a red message occurs this may be a sign that you might need to check your input to see if there are any errors. This could be from entering a duplicate habit, the incorrect password, or a username that doesn't exist. Else users would be redirected to a error page where you can be taken back to the website afterwards. ",
        "What types of customizability do you current offer": "Currently Hadit offers the ability to change from Light to Dark mode in the user info page. As well there is a page for cats incase you want to look at some adorable cutie pies. ",
    }
    return render_template("faq.html", faqs=faqs)


@app.route("/cats", methods=["get"])
def cats():
    return render_template("cats.html")

"""
@app.errorhandler(400)
def bad_request(error):
    return (
        render_template(
            "error.html",
            error_code=400,
            error_description="Bad Request",
            error_message="Sorry, there was a problem with your request.",
        ),
        400,
    )


@app.errorhandler(401)
def unauthorized(error):
    return (
        render_template(
            "error.html",
            error_code=401,
            error_description="Unauthorized",
            error_message="Sorry, you don't have access to this page.",
        ),
        401,
    )


@app.errorhandler(403)
def forbidden(error):
    return (
        render_template(
            "error.html",
            error_code=403,
            error_description="Forbidden",
            error_message="Sorry, you don't have permission to access this page.",
        ),
        403,
    )


@app.errorhandler(404)
def page_not_found(error):
    return (
        render_template(
            "error.html",
            error_code=404,
            error_description="Page Not Found",
            error_message="Sorry, we couldn't find the page you were looking for.",
        ),
        404,
    )


@app.errorhandler(405)
def method_not_allowed(error):
    return (
        render_template(
            "error.html",
            error_code=406,
            error_description="Method Not Allowed",
            error_message="Sorry, the method you used to access this page is not allowed.",
        ),
        405,
    )


@app.errorhandler(500)
def internal_server_error(error):
    db.session.rollback()
    return (
        render_template(
            "error.html",
            error_code=500,
            error_description="Internal Server Error",
            error_message="Sorry, there was an internal server error.",
        ),
        500,
    )


@app.errorhandler(IntegrityError)
def handle_integrity_error(error):
    db.session.rollback()
    flash("Integrity error occurred")
    return redirect(url_for("register"))


@app.errorhandler(Exception)
def handle_all_other_errors(error):
    db.session.rollback()
    flash("An error occurred")
    return (
        render_template(
            "error.html",
            error_code=500,
            error_description="Internal Server Error",
            error_message="Sorry, there was an internal server error.",
        ),
        500,
    )
"""