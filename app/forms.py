# neccesary imports for forms classes and dunctions
from flask_wtf import FlaskForm, Recaptcha, RecaptchaField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms import (
    StringField,
    SubmitField,
    PasswordField,
    TextAreaField,
    RadioField,
    HiddenField
)

"""
Form for creating habits
Takes paramters of name which is the anme of the habit
The type of habit whether it is good or bad, Used with points function
Reason is text area field for why users wants to do habit
"""

class HabitForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    type_of_habit = RadioField(choices=(['bad', 'Habit to Break'], [
                               'good', 'Habit to build']), validators=[DataRequired()])
    reason = TextAreaField("reason", validators=[
                           DataRequired(), Length(8, 64)])
    submit = SubmitField("submit")


class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField("submit")

# Form for registering users

class RegisterForm(FlaskForm):
    username = StringField("username", validators=[
                           DataRequired(), Length(6, 24)])
    email = StringField("email", validators=[DataRequired(), Email()])
    # Email field for user and checks if email follows valid patternn with Email() validator
    password1 = PasswordField("Password", validators=[
                              DataRequired(), Length(12, 64)])
    password2 = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password1")]
    )
    # Check to make sure there not a robot
    recaptcha = RecaptchaField("Recaptcha", validators=[
                               Recaptcha()])
    # Setup of flask-wtforms google recaptcha field
    register = SubmitField("register")


class YesNo(FlaskForm):
    options = RadioField(choices=(["y", "Yes"], ["n", "No"]))
    submit = SubmitField("Submit")

# Used on dashboard page when determine that habit to update in streak table

class StreakForm(FlaskForm):
    hidden_id = HiddenField(name='habit_id')
    submit = SubmitField('Done')
    update =SubmitField('Update')
    delete= SubmitField('Delete')

# Form for user updating reason for why they do a habit

class UpdateForm(FlaskForm):
    reason = TextAreaField(name='updated_reason', validators=[
                           DataRequired(), Length(8, 64)])
    submit = SubmitField('update')

class ShopForm(FlaskForm):
    theme_customization= SubmitField('Customize')
    streak_freeze=SubmitField('Purchase Streak Freeze')