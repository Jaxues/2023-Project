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


class HabitForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    reason = TextAreaField("reason", validators=[DataRequired(), Length(8,64)])
    submit = SubmitField("submit")


class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField("submit")

# Form for registering users


class RegisterForm(FlaskForm):
    username = StringField("username", validators=[DataRequired(), Length(6,24)])
    email = StringField("email", validators=[DataRequired(), Email()])
    # Email field for user and checks if email follows valid patternn with Email() validator
    password1 = PasswordField("Password", validators=[DataRequired(), Length(12,64)])
    password2 = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password1")]
    )
    recaptcha = RecaptchaField("Recaptcha", validators=[
                               Recaptcha(),])
    # Setup of flask-wtforms google recaptcha field
    register = SubmitField("register")


class YesNo(FlaskForm):
    options = RadioField(choices=(["y", "Yes"], ["n", "No"]))
    submit = SubmitField("Submit")


class StreakForm(FlaskForm):
    hidden_id = HiddenField(name='habit_id')
    submit = SubmitField('Done')


class UpdateForm(FlaskForm):
    reason = TextAreaField(name='updated_reason', validators=[DataRequired(), Length(8,64)])
    submit = SubmitField('update')
