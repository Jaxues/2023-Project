from app import app, forms, db, login_manager
from flask import render_template, url_for, redirect, flash, jsonify
from app.models import habits, users, streak
from flask_login import login_required, current_user, logout_user, login_user
from werkzeug.security import check_password_hash
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import StaleDataError
from app.function import get_local_date, check_consecutive, heatmap_data, heatmap_date_checker
from better_profanity import profanity


@login_manager.user_loader
# Define userloader to Users ID
def load_user(user_id):
    # Create function
    # Returns current users_id from 'users' table
    return users.query.get(user_id)


@app.route("/login", methods=["get", "post"])
# define login route
def login():
    # Create login function
    form = forms.LoginForm()
    # Set form variable to be equal to Loginform class from forms.py
    if current_user.is_authenticated:
        # If current users is already logged in flash message
        flash("error", "Your already logged in silly :)")
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
                flash("success", "Login Succeesful")
                # Alert user that proccess was succesful
                return redirect(url_for("dashboard"))
            # Return to page where user can see most recent habits
            else:
                flash("error","Wrong password")
                # If user entered password is incorrect. Won't log in user
        else:
            flash("error","User doesn't exist")
            # If user isn't created alert user
    return render_template("login.html", form=form)


@app.route("/register", methods=["get", "post"])
# Define register route
def register():
    form = forms.RegisterForm()
    if current_user.is_authenticated:
        # If current users is already logged in flash message
        flash("error", "Your already logged in silly :)")
        return redirect(url_for("info"))

    # Set form variable to be equal to RegisterForm class from forms.py
    if form.validate_on_submit():
        # Once user has succesfully submited form
        profanity_username = profanity.contains_profanity(form.username.data)
        profanity_password = profanity.contains_profanity(form.password1.data)
        profanity_email = profanity.contains_profanity(form.email.data)
        if profanity_username or profanity_password or profanity_email:
            flash('error', 'Details contain profanity please remove it')
            return redirect(url_for('register'))
        else:
            newuser = users(username=form.username.data, email=form.email.data)
        # set newuser variable to be equal to have username and email to same as entered credentials
            newuser.set_password(form.password1.data)
        # Set password hash for new user
            if form.password1.data != form.password2.data:
                flash('error',"Password's don't match check them again.")
                return redirect(url_for('regiter'))
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
            flash("error", "User already exists")
            return redirect(url_for('register'))
        except:
            flash('error',"There was an error in adding user. Pleae try again")
            return redirect(url_for('register'))
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
            flash("error", "You already have this habit")
            return redirect(url_for("addhabit"))
        else:
            profanity_check_habit = profanity.contains_profanity(
                form.name.data)
            profanity_check_reason = profanity.contains_profanity(
                form.reason.data)
            profanitY_check_habit_censor= profanity.censor(form.name.data)
            profanity_check_reason_censor = profanity.censor(form.reason.data)
            for test_charatcer in profanity_check_reason_censor: 
                if test_charatcer=='*':
                    flash('error', 'This has profanity. That or you have entered an asteriks. Either is not allowed')
                    return redirect(url_for('addhabit'))
            for test_reason in profanitY_check_habit_censor:
                if test_reason == '*':
                    flash('error', 'This contains an asteriks. Either this was censored by the filter or you have entered an astericks. Either way please remove this')
                    return redirect(url_for('addhabit'))
            if profanity_check_habit or profanity_check_reason:
                flash('error','This contains profanity please remove this.')
                return redirect(url_for('addhabit'))
            else:
                NewHabit = habits(
                    name=form.name.data.title(),
                    reason=form.reason.data.title(),
                    user_id=current_user.id,
                )
                db.session.add(NewHabit)
                db.session.commit()
                flash("success", "Habit added successfully!")
                return redirect(url_for("dashboard"))
    return render_template("addHabit.html", form=form)


@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    Habits = habits.query.filter_by(user_id=current_user.id)
    Streaks = streak.query.filter_by(user_id=current_user.id)
    user_streaks={}
    for Habit in Habits:
        add_user_streak=streak.query.filter_by(user_id=current_user.id, habit_id=Habit.id).order_by(streak.date.desc()).first()
        recent_date=add_user_streak.date
        recent_streak=add_user_streak.is_consecutive
        user_streaks[recent_date]=recent_streak
    form = forms.StreakForm()
    if form.validate_on_submit():
        habit_id = form.hidden_id.data
        current_date = get_local_date()
        check_entry = streak.query.filter_by(
            user_id=current_user.id, habit_id=habit_id, date=current_date).first()
        if check_entry:
            flash("error", "You have already reccorded your habit for today. ")
            print(check_entry)
            return redirect(url_for('dashboard'))

        check_date = streak.query.filter(
            streak.user_id == current_user.id,
            streak.habit_id == habit_id,
            streak.date < current_date
        ).order_by(streak.date.desc()).first()

        if check_date:
            streak_score = check_consecutive(check_date)
            new_entry = streak(user_id=current_user.id,
                               habit_id=habit_id, date=current_date, is_consecutive=streak_score)
        else:
            new_entry = streak(user_id=current_user.id,
                               habit_id=habit_id, date=current_date, is_consecutive=1)
        db.session.add(new_entry)
        db.session.commit()
        # Call the method to check consecutive streaks
        flash('success', 'Streak successfully recorded')
    return render_template("dashboard.html", Habits=Habits, Streaks=Streaks, form=form, user_streaks=user_streaks)


@app.route("/delete/<int:id>")
@login_required
def delete(id):
    habit_to_delete = habits.query.filter_by(
        id=id).first()
    if habit_to_delete.user_id != current_user.id:
        flash('error',"You don't own this habit. You can't delete it")
        return redirect(url_for('dashboard'))
    streaks_to_delete = streak.query.filter_by(habit_id=id)
    for streak_to_delete in streaks_to_delete:
        db.session.delete(streak_to_delete)

    try:
        db.session.delete(habit_to_delete)
        db.session.commit()
        flash('success', 'Habit successfully deleted.')
    
    except:
        db.session.rollback()
        flash('error', 'An error occurred while deleting the habit.') 

    return redirect(url_for('dashboard'))


@app.route("/update/<int:id>", methods=['GET', 'POST'])
@login_required
def update(id):
    current_habit=habits.query.filter_by(id=id).first()
    if current_habit is None:
        flash("error","This habit doesn't exist you can't delete this")
        return redirect(url_for('dashboard'))
    if current_habit.user_id != current_user.id:
        flash('error', "You don't own this habit you can't update it.")
        return redirect(url_for('dashboard'))
    form = forms.UpdateForm() 
    if form.validate_on_submit():
        habit = habits.query.filter_by(id=id).first()
        updated_reason = form.reason.data
        check_profanity_reason=profanity.contains_profanity(updated_reason)
        if check_profanity_reason:
            flash('error','This updated reason contains profanity please remove it if you wish to update it.')
            return redirect(url_for('dashboard')) 
        habit.reason = updated_reason
        db.session.commit()
        flash('success', 'Reason succesfully updated')
        return redirect(url_for('dashboard'))
    return render_template('Update.html', form=form, current_habit=current_habit)


@app.route("/info")
def info():
    if current_user.is_authenticated:
        form = forms.YesNo()
        if form.validate_on_submit():
            email_perference = form.options.data
            print(email_perference)
            return (redirect('subscribe'))
        return render_template("info.html", form=form)
    else:
        flash("You haven't logged on you can't access this page")
        return redirect(url_for("login"))

# Email perferences to subscribe user to email


@app.route("/subscribe", methods=['GET', 'POST'])
@login_required
def subscribe():
    email_user = users.query.filter_by(id=current_user.id).first()
    if email_user.email_notifactions == True:
        email_user.email_notifcations = False
    elif email_user.email_notifactions == False:
        email_user.email_notifactions = True
    db.session.add(email_user)
    db.session.commit()
    flash('success', 'Email perferences updated')
    return redirect(url_for('info'))


@app.route("/faq", methods=["get"])
def faq():
    faqs = {
        "What is this app about?": "Hadit is a habit tracker meant to help neurodivergent people as well as thoose with psychological conditions. By offering a customizable and more engaging way for people to achieve there habits",
        "How do I create an account?": "Go onto signup page. Enter your email, username, password. And then do recaptcha to make sure your not a robot. Afterwards if all your details are valid you should be logged in.",
        "How do I add a new habit?": "First sign into your account or create a new account <a href="+ url_for('register')+ ">signup page</a> Afterwards navigate to add habit route and enter the details or your habit and optionally enter the reason you want to do your habit.",
        "How do I check off a completed habit?": "Make sure you are signed into your account. Navigate to dashboard and then select the checkbox if you have done your habit.",
        "Can I use this app on multiple devices?": "Yes, Hadit is a website created using Flask, HTML, CSS, and Javascript. And is capable of running on any modern webbrowser without any need for any special configuration. Just sign into your account and your informaton should sync from you account seamlessly. ",
        "Is my personal information secure on this app?": "Yes. Hadit hashes all the passwords from users as well as encrypting any text entered for the reason user input for habits. To try to ensure users privacy. for more information go to <a href="+ url_for('privacy')+"> privacy page </a> for more information",
        "What happens if I encounter an error or bug?": "If a red message occurs this may be a sign that you might need to check your input to see if there are any errors. This could be from entering a duplicate habit, the incorrect password, or a username that doesn't exist. Else users would be redirected to a error page where you can be taken back to the website afterwards. ",
        "What types of customisability do you current offer": "Currently Hadit offers the ability to change from Light to Dark mode in the user info page. As well there is a page for cats in case you want to look at some adorable cutie pies. ",
        "Do I need to do neurodivergent or have a psychological condition to use this app":"No, of course not. Hadit is primaryily devolped for this audience but in doing so it also tries to make itself more accessible to everyone.",
        "What are some words censored in the profanity filter":" Due to using an external api I can't control what words are censored. This is not to supress peoples expression but as a precaution to stop offensive statements."
    }
    return render_template("faq.html", faqs=faqs)

@app.route("/privacy", methods=["get","post"])
def privacy():
    privacy_policy = {
        'Collection of Personal Data': 'Hadit does not collect any personal data from our users. We believe in respecting your privacy and ensuring that your information remains confidential.',
        'Encryption and Data Security': 'All text information uploaded to Hadit is encrypted to provide an additional layer of protection. We utilize industry-standard encryption algorithms to safeguard your data. Rest assured that only you, as the user, can access your information.',
        'Password Protection': 'To ensure the security of your account, we use password hashing techniques to store your passwords. This means that your passwords are transformed into a secure, irreversible format. We strongly recommend using unique and strong passwords to further enhance your account\'s security.',
        'Email Address Verification': 'As part of our security measures, users are required to verify their email address during the registration process. This helps us confirm the authenticity of user accounts and prevents unauthorized access.',
        'Account Registration with Recaptcha': 'To prevent automated bots and ensure a secure registration process, we employ Recaptcha, a widely-used security measure. This helps us verify that the registration is being performed by a human user and not by malicious software.',
        'Third-Party Services': 'Please note that while we take utmost care in protecting your personal data, Hadit may contain links to third-party websites or services. We encourage you to review the privacy policies of these external sites as they may have different practices and policies.',
        'Compliance with Legal Requirements': 'Hadit is committed to complying with all applicable laws and regulations regarding data protection and user privacy. We will cooperate with law enforcement authorities and regulatory agencies as required by law.',
        'Updates to the Privacy Policy': 'We reserve the right to update this Privacy Policy at any time. Changes will be effective immediately upon posting on this page. We encourage you to review this policy periodically to stay informed about how we protect your personal information.'
    }

    return render_template('pp.html', privacy_policy=privacy_policy)

"""
def bad_request(error):
    if app.config['TESTING']:
        pass
    else:
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
    if app.config['TESTING']:
        pass
    else:
 
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
    if app.config['TESTING']:
        pass
    else:
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
    if app.config['TESTING']:
        pass
    else:
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
    if app.config['TESTING']:
        pass
    else:
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
    if app.config['TESTING']:
            pass
    else:
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
    if app.config['TESTING']:
        pass
    else:
        return ( render_template(
            "error.html",
            error_code=500,
            error_description="Internal Server Error",
            error_message="Sorry, there was an internal server error.",),
            500,
        )
@app.route('/cat')
def catpage():
    return render_template('cats.html')


"""