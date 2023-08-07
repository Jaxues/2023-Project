# Import necessary models to get routes working
from app import (
    app, db, login_manager, serializer
)
from flask import (
    render_template, url_for, redirect, flash, jsonify
)
from app.models import (
    Habits, Users, Streak, UserTheme, Achievements, UserAchievements
)
from app.forms import (
    HabitForm, StreakForm, LoginForm,
    RegisterForm, UpdateForm, YesNo, ShopForm,
    ThemeForm
)
from flask_login import (
    login_required, current_user, logout_user, login_user
)
from werkzeug.security import check_password_hash
from sqlalchemy.exc import IntegrityError
from app.function import (
    get_local_date, check_consecutive, heatmap_data,
    heatmap_date_checker, habit_points, email_verification,
)
from better_profanity import profanity
from math import ceil
from itsdangerous import SignatureExpired, BadSignature
from datetime import datetime, timedelta


@login_manager.user_loader
def load_user(user_id):
    # Define userloader to Users ID
    # Create function
    # Returns current users_id from 'users' table
    return Users.query.get(user_id)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        flash("error", "You are already logged in.")
        return redirect(url_for("info"))

    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password_hash, form.password.data):
                if user.email_authentication:
                    login_user(user)
                    flash("success", "Login successful!")
                    return redirect(url_for("dashboard", id=1))
                else:
                    token_date = user.date_joined
                    elapsed_time = datetime.now() - token_date
                    if elapsed_time > timedelta(1):
                        email_token = serializer.dumps(user.email)
                        email_verification(user.email, email_token)
                        flash('error', 'Email not verified. Another token was sent to email address')
                        return redirect(url_for('register'))
                    flash("error", "Please verify your email before logging in.")
                    return redirect(url_for("login"))
            else:
                flash("error", "Invalid username or password.")
        else:
            flash("error", "User does not exist.")

    return render_template("login.html", form=form)



@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if current_user.is_authenticated:
        flash("error", "You're already logged in silly :)")
        return redirect(url_for("info"))

    if form.validate_on_submit():
        profanity_username = profanity.contains_profanity(form.username.data)
        profanity_password = profanity.contains_profanity(form.password1.data)
        profanity_email = profanity.contains_profanity(form.email.data)
        if profanity_username or profanity_password or profanity_email:
            flash('error', 'Details contain profanity, please remove it')
            return redirect(url_for('register'))
        else:
            newuser = Users(username=form.username.data, email=form.email.data)
            newuser.set_password(form.password1.data)

            if form.password1.data != form.password2.data:
                flash("error", "Passwords don't match, check them again.")
                return redirect(url_for('register'))
            db.session.add(newuser)

            try:
                db.session.add(newuser)
                db.session.commit()
                email = form.email.data
                token = serializer.dumps(email)
                email_verification(email, token)
                flash('success', 'Email needs to be authenticated, an email was sent to {}'.format(email))
                return redirect(url_for("login"))
            except IntegrityError:
                db.session.rollback()
                flash("error", "User already exists")
                return redirect(url_for('register'))
    
    return render_template("register.html", form=form)

@app.route('/authenticate/<token>', methods=['get','post'])
def authentication(token):
    form=LoginForm()
    if current_user.is_authenticated:
        flash('error','You are already logged in.')
        return redirect(url_for('dashboard',id=1))
    if form.validate_on_submit():
        authenticate_user=Users.query.filter_by(username=form.username.data).first()
        if authenticate_user:
            try:
                email_token=serializer.loads(token, max_age=3600)
                if authenticate_user.email_authentication:
                    flash('error','This user is already verified')
                    return redirect(url_for('login'))
                if check_password_hash(authenticate_user.password_hash,form.password.data):
                    authenticate_user.email_authentication=True
                    db.session.commit()
                    authenticated_achievement=UserAchievements(user_id=authenticate_user.id, achievement_id=20)
                    db.session.add(authenticated_achievement)
                    db.session.commit()
                    login_user(authenticate_user)
                    flash('success','Email Verified.')
                    return redirect(url_for('dashboard',id=1))
                else:
                    flash('error', "Password doesn't match please try again")
                    return redirect(url_for('authentication',token=token))
            except SignatureExpired:
                flash('error','Token has expired')
                return redirect(url_for('register'))
            except BadSignature:
                flash('error','Invalid email token.')
                return redirect(url_for('register'))
        else:
                flash('error', "user doesn't exist please register first")
                return redirect(url_for('register'))
    return render_template('authenticate.html',form=form, token=token)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/addhabit", methods=["GET", "POST"])
@login_required
def addhabit():
    form = HabitForm()
    if form.validate_on_submit():
        # See if habit exists if it does then flash message to stop duplicates
        checkhabit = Habits.query.filter_by(user_id=current_user.id, name=form.name.data.title()).first()
        print('Habit Added')
        if checkhabit:
            flash("error", "You already have this habit")
            return redirect(url_for("addhabit"))
        else:
            # Check for profanity and stop it
            profanity_check_habit = profanity.contains_profanity(form.name.data)
            profanity_check_reason = profanity.contains_profanity(form.reason.data)
            profanitY_check_habit_censor = profanity.censor(form.name.data)
            profanity_check_reason_censor = profanity.censor(form.reason.data)
            for test_character in profanity_check_reason_censor:
                if test_character == '*':
                    flash(
                        'error', 'This has profanity. That or you have entered an asterisk. Either is not allowed')
                    return redirect(url_for('addhabit'))
            for test_reason in profanitY_check_habit_censor:
                # Loop to go through all words that users enter even if they space words out will censor it.
                if test_reason == '*':
                    flash('error', 'This contains an asterisk. Either this was censored by the filter or you have entered an asterisk. Either way please remove this')
                    return redirect(url_for('addhabit'))
            if profanity_check_habit or profanity_check_reason:
                flash('error', 'This contains profanity please remove this.')
                return redirect(url_for('addhabit'))
            else:
                NewHabit = Habits(
                    name=form.name.data.title(),
                    reason=form.reason.data.title(),
                    habit_type=form.type_of_habit.data,
                    user_id=current_user.id
                )
                db.session.add(NewHabit)
                db.session.commit()
                flash("success", "Habit added successfully!")
                # Return first page of dashboard page. Dashboard indexed so the first page only has 3 habits on it.
                return redirect(url_for("dashboard", id=1))
    return render_template("addHabit.html", form=form)


@app.route("/dashboard/<int:id>", methods=['GET', 'POST'])
@login_required
def dashboard(id):
    habits = Habits.query.filter_by(user_id=current_user.id)
    user_streaks = {}
    total_habits = habits.count() if habits else 0
    habits_first_page = 3
    habits_pages = 5
    # See how many pages are needed to display all habits for the user.
    total_pages = ceil(((total_habits - habits_first_page) / habits_pages) + 1)

    if id == 0:
        return redirect(url_for('dashboard', id=1))
    if id > total_pages:
        return redirect(url_for('dashboard', id=total_pages))

    for habit in habits:
        Habit_streak = Streak.query.filter_by(habit_id=habit.id).order_by(Streak.date.desc())
        if Habit_streak.first():
            user_streaks[habit.id] = [Habit_streak.first().is_consecutive, Habit_streak.first().date]
        else:
            user_streaks[habit.id] = [0, 'No date recorded']

    form = StreakForm()
    preprocess_data = heatmap_data(Streak.query.filter_by(user_id=current_user.id))
    check_days = heatmap_date_checker(preprocess_data)
    # convert data from the database to a suitable format for JSON
    frontend_heatmap_data = check_days

    if form.validate_on_submit():
        habit_id = form.hidden_id.data
        if form.update.data:
            return redirect(url_for('update', id=habit_id))
        elif form.delete.data:
            return redirect(url_for('delete', id=habit_id))
        else:
            current_date = get_local_date()
            check_entry = Streak.query.filter_by(user_id=current_user.id, habit_id=habit_id, date=current_date).first()
            # Query the streak database, so can't have multiple of the same entry
            if check_entry:
                flash("error", "You have already recorded your habit for today.")
                return redirect(url_for('dashboard', id=1))

            check_date = Streak.query.filter(
                Streak.user_id == current_user.id,
                Streak.habit_id == habit_id,
                Streak.date < current_date
            ).order_by(Streak.date.desc()).first()
            # See if the previous entry was the day before
            if check_date:
                filtered_type_of_habit = Habits.query.filter_by(id=form.hidden_id.data).first()
                streak_score = check_consecutive(streak_parameter=check_date, user=current_user)
                new_entry = Streak(user_id=current_user.id,
                                   habit_id=habit_id, date=current_date, is_consecutive=streak_score)
                if streak_score == 7 and UserAchievements.query.filter_by(user_id=current_user.id, achievement_id=1).first() is None:
                    bronzestreakachievement=UserAchievements(user_id=current_user.id, achievement_id=1)
                    db.session.add(bronzestreakachievement)
                    db.session.commit()
                if streak_score == 14 and UserAchievements.query.filter_by(user_id=current_user.id, achievement_id=1).first() is None:
                    bronzestreakachievement=UserAchievements(user_id=current_user.id, achievement_id=1)
                    db.session.add(bronzestreakachievement)
                    db.session.commit()
                if streak_score == 30 and UserAchievements.query.filter_by(user_id=current_user.id, achievement_id=1).first() is None:
                    bronzestreakachievement=UserAchievements(user_id=current_user.id, achievement_id=1)
                    db.session.add(bronzestreakachievement)
                    db.session.commit()



            # If dates aren't consecutive, assign a streak of 1 for the first day of recording the habit
            else:
                new_entry = Streak(user_id=current_user.id,
                                   habit_id=habit_id, date=current_date, is_consecutive=1)

            user_streak = Streak.query.filter_by(id=current_user.id, habit_id=habit_id).order_by(
                Streak.date.desc()).first()
            user_habit = Habits.query.filter_by(id=habit_id, user_id=current_user.id).first()

            if user_streak:
                # Give users points based on whether they have a streak already
                print(user_habit.habit_type)
                add_points = habit_points(user_streak.is_consecutive, user_habit.habit_type, user=current_user)
            else:
                # Assign points with no streak entries
                add_points = habit_points(0, user_habit.habit_type, user=current_user)

            current_user.user_points = current_user.user_points + add_points
            if current_user.user_points== 10000 and UserAchievements.query.filter_by(user_id=current_user.id, achievement_id=19).first() is None:
                diamond_points=UserAchievements(user_id=current_user.id, achievement_id=19)
                db.session.add(diamond_points)
                db.session.commit()
            type_habit=Habits.query.filter_by(id=form.hidden_id.data).first()
            if type_habit.habit_type == 1:
                current_user.good_habits_tracked += 1
                if current_user.good_habits_tracked == 7 and UserAchievements.query.filter_by(user_id=current_user.id, achievement_id=4).first() is None:
                    bronzegoodhabit=UserAchievements(user_id=current_user.id, achievement_id=4)
                    db.session.add(bronzegoodhabit)
                    db.session.commit()
                    achievement_info=Achievements.query.get(id=4)
                    flash("achievement","You earned the {} achievement for {}".format(str(achievement_info.name).lower(), str(achievement_info.description).lower()))
                if current_user.good_habits_tracked == 14 and UserAchievements.query.filter_by(user_id=current_user.id, achievement_id=5).first() is None:
                    silvergoodhabit=UserAchievements(user_id=current_user.id, achievement_id=5)
                    db.session.add(silvergoodhabit)
                    db.session.commit()
                    achievement_info=Achievements.query.get(id=5)
                    flash("achievement","You earned the {} achievement for {}".format(str(achievement_info.name).lower(), str(achievement_info.description).lower()))
                if current_user.good_habits_tracked ==30 and UserAchievements.query.filter_by(user_id=current_user.id, achievement_id=6).first() is None:
                    goldgoodhabit=UserAchievements(user_id=current_user.id, achievement_id=6)
                    db.session.add(goldgoodhabit)
                    db.session.commit()
                    achievement_info=Achievements.query.get(id=6)
                    flash("achievement","You earned the {} achievement for {}".format(str(achievement_info.name).lower(), str(achievement_info.description).lower()))

            else:
                current_user.bad_habits_tracked +=1
                if current_user.bad_habits_tracked == 7 and UserAchievements.query.filter_by(user_id=current_user.id, achievement_id=7).first() is None:
                    bronzebadhabit=UserAchievements(user_id=current_user.id, achievement_id=7)
                    db.session.add(bronzebadhabit)
                    db.session.commit()
                    achievement_info=Achievements.query.get(id=7)
                    flash("achievement","You earned the {} achievement for {}".format(str(achievement_info.name).lower(), str(achievement_info.description).lower()))
                if current_user.bad_habits_tracked == 14 and UserAchievements.query.filter_by(user_id=current_user.id, achievement_id=8).firt() is None:
                    silverbadhabit=UserAchievements(user_id=current_user.id, achievement_id=8)
                    db.session.add(silverbadhabit)
                    db.session.commit()
                    achievement_info=Achievements.query.get(id=8)
                    flash("achievement","You earned the {} achievement for {}".format(str(achievement_info.name).lower(), str(achievement_info.description).lower()))
                if current_user.bad_habits_tracked ==30 and UserAchievements.query.filter_by(user_id=current_user.id, achievement_id=9).first() is None:
                    goldbadhabit=UserAchievements(user_id=current_user.id, achievement_id=9)
                    db.session.add(goldbadhabit)
                    db.session.commit()
                    achievement_info=Achievements.query.get(id=9)
                    flash("achievement","You earned the {} achievement for {}".format(str(achievement_info.name).lower(), str(achievement_info.description).lower()))
            db.session.commit()
            db.session.add(new_entry)
            db.session.commit()
            # Call the method to check consecutive streaks
            flash('success', 'Streak successfully recorded. You earn {} points'.format(add_points))
            return redirect(url_for('dashboard', id=1))

    if total_habits > 0:
        return render_template("dashboard.html", Habits=habits, user_streak=user_streaks, form=form, id=id, habits_first_page=habits_first_page, habits_per_page=habits_pages, total_pages=total_pages, frontend_heatmap_data=frontend_heatmap_data)
    else:
        return render_template("dashboard.html", Habits=None, user_streak=None, form=form, id=id, habits_first_page=habits_first_page, habits_per_page=habits_pages, total_pages=total_pages, frontend_heatmap_data=frontend_heatmap_data)


@app.route("/delete/<int:id>")
@login_required
def delete(id):
    habit_to_delete = Habits.query.filter_by(
        id=id).first()
    # Stop unathorised users from deleting habits they don't own
    if habit_to_delete.user_id != current_user.id:
        flash('error', "You don't own this habit. You can't delete it")
        return redirect(url_for('dashboard', id=1))
    try:
        # Delete all streak entries for the habit
        streak_records = Streak.query.filter_by(habit_id=id).all()
        for record in streak_records:
            db.session.delete(record)
        db.session.delete(habit_to_delete)
        db.session.commit()
        flash('success', 'Habit successfully deleted.')

    except:
        db.session.rollback()
        flash('error', 'An error occurred while deleting the habit.')

    return redirect(url_for('dashboard', id=1))


@app.route("/update/<int:id>", methods=['GET', 'POST'])
@login_required
def update(id):
    current_habit = Habits.query.filter_by(id=id).first()
    # Check if habit exists
    if current_habit is None:
        flash("error", "This habit doesn't exist you can't update it.")
        return redirect(url_for('dashboard', id=1))
    # See if user owns the habit they want to update
    if current_habit.user_id != current_user.id:
        flash('error', "You don't own this habit you can't update it.")
        return redirect(url_for('dashboard', id=1))
    form = UpdateForm()
    if form.validate_on_submit():
        habit = Habits.query.filter_by(id=id).first()
        name=form.name.data
        updated_reason = form.reason.data
        check_profanity_reason = profanity.contains_profanity(updated_reason)
        # Check for profanity in user inputted reason
        if check_profanity_reason:
            flash(
                'error', 'This updated reason contains profanity please remove it if you wish to update it.')
            return redirect(url_for('dashboard', id=1))
        habit.reason = updated_reason
        habit.name=name
        db.session.commit()
        flash('success', 'Reason succesfully updated')
        return redirect(url_for('dashboard', id=1))
    return render_template('Update.html', form=form, current_habit=current_habit)


@app.route("/info", methods=['get','post'])
def info():
    # See if user has logged in
    if current_user.is_authenticated:
        form = YesNo()
        total_user_achievements=UserAchievements.query.all()
        achievement_percentage=int(len(total_user_achievements))/20*100
        if achievement_percentage==0.25 and UserAchievements.query.filter_by(user_id=current_user.id, achievement_id=15).first() is None:
            bronze_progression=UserAchievements(user_id=current_user.id, achievement_id=15) 
            db.session.add(bronze_progression)
            db.session.commit()
        if achievement_percentage==0.5 and UserAchievements.query.filter_by(user_id=current_user.id, achievement_id=15).first() is None:
            silver_progression=UserAchievements(user_id=current_user.id, achievement_id=16) 
            db.session.add(silver_progression)
            db.session.commit()
        if achievement_percentage==0.75 and UserAchievements.query.filter_by(user_id=current_user.id, achievement_id=15).first() is None:
            gold_progression=UserAchievements(user_id=current_user.id, achievement_id=17) 
            db.session.add(gold_progression)
            db.session.commit()
        if achievement_percentage==0.95 and UserAchievements.query.filter_by(user_id=current_user.id, achievement_id=15).first() is None:
            complete_progression=UserAchievements(user_id=current_user.id, achievement_id=18) 
            db.session.add(complete_progression)
            db.session.commit()
        if form.validate_on_submit():
            email_perference = form.options.data
            print(email_perference)
            if email_perference == 'y':
                current_user.email_notifactions = True
                db.session.commit()
            elif email_perference == 'n':
                current_user.email_notifactions = False 
                db.session.commit()
            flash('success','Email perferences successfully updated')
            return redirect(url_for('info'))
        return render_template("info.html", form=form, achievement_percentage=achievement_percentage)
    else:
        flash("error","You haven't logged on you can't access this page")
        return redirect(url_for("login"))


@app.route("/faq", methods=["GET"])
def faq():
    # Store FAQ in backend to be dynamically updated and more efficient
    faqs = {
        "What is this app about?": "Hadit is a habit tracker meant to help neurodivergent people as well as those with psychological conditions. By offering a customizable and more engaging way for people to achieve their habits.",
        "How do I create an account?": "Go onto the signup page. Enter your email, username, password. And then do recaptcha to make sure you're not a robot. Afterwards, if all your details are valid, you should be logged in.",
        "How do I add a new habit?": "First, sign into your account or create a new account <a href=" + url_for('register') + ">signup page</a>. Afterwards, navigate to add a habit route and enter the details of your habit and optionally enter the reason you want to do your habit.",
        "How do I check off a completed habit?": "Make sure you are signed into your account. Navigate to the dashboard and then select the checkbox if you have done your habit.",
        "Can I use this app on multiple devices?": "Yes, Hadit is a website created using Flask, HTML, CSS, and Javascript. And is capable of running on any modern web browser without any need for any special configuration. Just sign into your account, and your information should sync from your account seamlessly.",
        "Is my personal information secure on this app?": "Yes. Hadit hashes all the passwords from users as well as encrypting any text entered for the reason user input for habits. To try to ensure users' privacy. For more information, go to <a href=" + url_for('privacy')+"> privacy page </a> for more information.",
        "What happens if I encounter an error or bug?": "If a red message occurs, this may be a sign that you might need to check your input to see if there are any errors. This could be from entering a duplicate habit, the incorrect password, or a username that doesn't exist. Else users would be redirected to an error page where you can be taken back to the website afterwards.",
        "What types of customizability do you currently offer": "Currently, Hadit offers the ability to change from Light to Dark mode on the user info page. As well Hadit offer the ability to user to change to a custom theme by spending 4000 points on the <a href=" + url_for('shop')+"> shop page </a>. Note users need an account first",
        "Do I need to be neurodivergent or have a psychological condition to use this app": "No, of course not. Hadit is primarily developed for this audience but in doing so, it also tries to make itself more accessible to everyone.",
        "What are some words censored in the profanity filter": "Due to using an external API, I can't control what words are censored. This is not to suppress people's expression but as a precaution to stop offensive statements.",
        "Why are there 'good' and 'bad habits' ?": "The reason for this distinction is between habits that we would like to build or try to do more of (good habits) as well as bad behavior users wish to stop doing (bad habits)."
    }
    return render_template("faq.html", faqs=faqs)


@app.route("/privacy", methods=["GET", "POST"])
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


@app.route('/shop', methods=['get','post'])
@login_required
def shop():
    form = ShopForm()
    if form.validate_on_submit():
        if form.streak_freeze.data:
            streak_freeze_user= Users.query.filter_by(id=current_user.id).first()
            if streak_freeze_user.streak_freeze:
                flash('error','Streak freeze already purchased') 
                return redirect(url_for('shop'))
            elif streak_freeze_user.user_points >= 500:
                if streak_freeze_user.streak_freeze:
                    flash("error","Streak freeze already active")
                    return redirect(url_for('shop'))
                streak_freeze_user.user_points = current_user.user_points - 500
                streak_freeze_user.streak_freeze= True
                if UserAchievements.query.filter_by(id=current_user.id, achievement_id=14).first() is None:
                    streak_freeze_achievement=UserAchievements(user_id=current_user.id,achievement_id=14)
                    db.session.add(streak_freeze_achievement)
                    db.session.commit()
                flash('success','Streak freeze purchased')
                db.session.commit()
                return redirect(url_for('shop'))
                
            else:
                flash('error','Not enough points to purchase streak freeze only have {}'.format(streak_freeze_user.user_points))
                return redirect(url_for('shop'))
        elif form.theme_customization.data:
            theme_customization_user=Users.query.filter_by(id=current_user.id).first()

            if theme_customization_user.user_points >= 4000:
                flash('success','Enough points to purchase custom theme')
                return redirect(url_for('customize'))
            else:
                flash('error','Not enough points to purchase theme customixation need 4000 only have {}'.format(theme_customization_user.user_points)) 
                return redirect(url_for('shop'))

    return render_template('shop.html', form=form)

@app.route('/achivements')
@login_required
def user_achievement():
    total_achievements=[]
    current_achievements=UserAchievements.query.all()
    
    if current_achievements:
        for user_completed in current_achievements:
            achievement=Achievements.query.filter_by(id=user_completed.achievement_id).first()
            total_achievements.append(achievement)
    else:
        flash("error","no achievements created")

    return render_template('achivements.html', achievements=total_achievements)

@app.route('/theme', methods=['GET', 'POST'])
@login_required
def customize():
    """
    Customizes the theme for the user.

    Returns:
        If successful, redirects to the dashboard page.
        If there are errors, renders the customtheme.html template with the form.
    """
    # Check if the user has the required amount of points
    if current_user.user_points < 4000:
        flash('error', 'You need 4000 points to purchase theme customization. You only have {} points'.format(current_user.user_points))
        return redirect(url_for('shop'))
    
    form = ThemeForm()
    if form.validate_on_submit():
        user_custom_theme = Users.query.filter_by(id=current_user.id).first()
        primary_color = form.primary_color.data
        secondary_color = form.secondary_color.data
        accent_color = form.accent_color.data
        background_color = form.background_color.data
        color_fields = [primary_color.lower(), secondary_color.lower(), accent_color.lower(), background_color.lower()]
        if len(color_fields) != len(set(color_fields)):
            flash('error', 'Colors must be unique.')
            return redirect(url_for('customize'))

        # Process the submitted colors as needed
        user_custom_theme.user_points -= 4000
        print(primary_color, secondary_color, accent_color, background_color)
        theme_status = user_custom_theme.custom_theme
        if theme_status:
            # If the user already purchased a custom theme, delete the old entry to replace it.
            theme_to_delete = UserTheme.query.filter_by(id=current_user.id).first()
            db.session.delete(theme_to_delete)
            db.session.commit()
        
        check_theme_achievement=UserAchievements.query.filter_by(user_id=current_user.id, achievement_id=13).first()
        if check_theme_achievement is None:
            award_theme_achievement=UserAchievements(user_id=current_user.id, achievement_id=13)
            db.session.add(award_theme_achievement)
            flash('achievement','You earned the custom theme achievement')

        # Pass user input values to store user's preferred choices in the theme
        new_custom_theme = UserTheme(user_id=current_user.id, primary=primary_color, secondary=secondary_color, accent=accent_color, background=background_color)
        db.session.add(new_custom_theme)
        user_custom_theme.custom_theme = True
        db.session.commit()

        # Redirect or render a success message
        flash('success', 'Theme customization successful!')
        return redirect(url_for('dashboard', id=1))

    return render_template('customtheme.html', form=form)

# Custom error handler for app
def handle_bad_request(error):
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
def handle_unauthorized(error):
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
def handle_forbidden(error):
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
def handle_page_not_found(error):
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
def handle_method_not_allowed(error):
    return (
        render_template(
            "error.html",
            error_description="Method Not Allowed",
            error_message="Sorry, the method you used to access this page is not allowed.",
        ),
        405,
    )


@app.errorhandler(500)
def handle_internal_server_error(error):
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