# *IMPORTANT NOTE THIS CODE IS OUTDATED AND NOT SECURE I AM KEEPING THIS UP TO SHOWCASE MY PREVIOUS PROGRAMMING SKILLS ONLY* 
# 2023-Project
Welcome to Hadit my project for level 3 Programming. 
Hadit is a habit tracker for neurodivergent and people with pyschological conditions. 
To setup there are a couple steps
1. Move from github folder to standa alone
2. Load virtualenviorment and install requirements.txt

    ````bash
    hadit/scripts/activate
    pip install -r requirements.txt
    ````
    
2. Create a .env file and include in it the following
    - secret_key for setup of database and admin. This can be any value
    - recap_pub public key for google recaptcha. This is a value from google
    - recap_priv private key for google recaptcha. This is another value from gooogle
    - encryption_key used for encryption of database. This caa be anything
    - MAIL_USERNAME for sender of email. Real gmail address
    - MAIL_PASSWORD for password of sender. Password for same gmail address
    - serializer_key for setting value for token. This can be any value
3. Enter flask shell and create database. By importing db from app. And then 'db.create_all()'
4. Import helper function to add achievements by entering this "From app.achievement_stuff import add_achievements"
5. Call function. This creates all the achievements and inserts them into the database. "add_achievements()"

This is the intial setup and the app should now work. 
It includes encrypted database, google recaptcha, email reminders and email authentication

To disable any of the features do the following

## Recaptcha
Remove the folliwng lines of code from forms.py

```python 
recaptcha = RecaptchaField("Recaptcha", validators=[Recaptcha()])
``` 

And the following from register.html
```html
<div class="recaptcha">
       {{form.recaptcha}}        
</div>
```

## Encryption
Remove any instances of Encrypted Type.
Data saved should now be saved as plain text.

## Email 
Remove following code from init.py

``` python
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = environ['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = environ['MAIL_PASSWORD']
app.config['MAIL_DEFAULT_SENDER'] = environ['MAIL_USERNAME']
mail = Mail(app)
serializer_key = environ.get('serializer_key')
serializer = URLSafeTimedSerializer(serializer_key)
```

As well delete the following functions 
```python 
def email_verification(user_email, token):
    msg = Message("Authentication link", recipients=[user_email])
    msg.body = ("This is your authentication link {}. \n Remember to log in with your defined username and password from registration.".format(url_for('authentication', token=token, _external=True)))
    return mail.send(msg)


def email_reminders(user_email, username):
    msg = Message('Habit Reminder', recipients=[user_email])
    msg.body = (" Hi {}, \n Reminder to make sure to log on to hadit and track your habits today".format(username))
    return mail.send(msg)
```
As well remove the following from routes 
```python
else:
                    token_date = user.date_joined
                    elapsed_time = datetime.now() - token_date
                    if elapsed_time > timedelta(1):
                        email_token = serializer.dumps(user.email)
                        email_verification(user.email, email_token)
                        flash('error',
                              'Email not verified. Another token was sent.')
                        return redirect(url_for('register'))
                    flash("error",
                          "Please verify your email before logging in.")
                    return redirect(url_for("login"))

... 


email = form.email.data
                token = serializer.dumps(email)
                email_verification(email, token)
                flash('success',
                      'Email needs to be authenticated, an email was sent to {}'.format(email))


@app.route('/authenticate/<token>', methods=['get', 'post'])
def authentication(token):
    form = LoginForm()
    if current_user.is_authenticated:
        flash('error', 'You are already logged in.')
        return redirect(url_for('dashboard', id=1))
    if form.validate_on_submit():
        authenticate_user = Users.query.filter_by(username=form.username.data).first()
        if authenticate_user:
            try:
                user_password = form.password.data
                email_token = serializer.loads(token, max_age=3600)
                if authenticate_user.email_authentication:
                    flash('error', 'This user is already verified')
                    return redirect(url_for('login'))
                if check_password_hash(authenticate_user.password_hash, user_password):
                    authenticate_user.email_authentication = True
                    db.session.commit()
                    new_user = authenticate_user.id
                    authenticated_achievement = UserAchievements(user_id=new_user,
                                                                 achievement_id=20)
                    db.session.add(authenticated_achievement)
                    db.session.commit()
                    login_user(authenticate_user)
                    flash('success', 'Email Verified.')
                    return redirect(url_for('dashboard', id=1))
                else:
                    flash('error', "Password doesn't match please try again")
                    return redirect(url_for('authentication', token=token))
            except SignatureExpired:
                flash('error', 'Token has expired')
                return redirect(url_for('register'))
            except BadSignature:
                flash('error', 'Invalid email token.')
                return redirect(url_for('register'))
        else:
            flash('error', "user doesn't exist please register first")
            return redirect(url_for('register'))
    return render_template('authenticate.html', form=form, token=token)

```

Please note in order to have email authentication you must have a sender address as well as password.
Remember to also enable third party apps for google
