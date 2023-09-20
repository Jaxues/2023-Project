from flask_wtf import FlaskForm, Recaptcha, RecaptchaField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms import (StringField,
                     SubmitField, PasswordField, TextAreaField,
                     RadioField, HiddenField)
from wtforms.widgets import ColorInput


class HabitForm(FlaskForm):
    """
    Form for creating habits.
    Parameters:
    - name: Name of the habit
    - type_of_habit: Type of habit (good or bad)
    - reason: Reason for wanting to do the habit
    """
    name = StringField("Name", validators=[DataRequired(), Length(5, 50)])
    type_of_habit = RadioField(
        choices=[("bad", "Habit to Break"), ("good", "Habit to Build")],
        validators=[DataRequired()]
    )
    reason = TextAreaField("Reason", validators=[DataRequired(), Length(8, 64)])
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    """
    Form for user login.
    Parameters:
    - username: User's username
    - password: User's password
    """
    username = StringField("Username", validators=[DataRequired(), Length(6, 24)])
    password = PasswordField("Password", validators=[DataRequired(), Length(12, 64)])
    submit = SubmitField("Submit")


class RegisterForm(FlaskForm):
    """
    Form for user registration.
    Parameters:
    - username: User's desired username
    - email: User's email address
    - password1: User's desired password
    - password2: Confirmation of user's desired password
    - recaptcha: Recaptcha validation field
    """
    username = StringField("Username", validators=[DataRequired(), Length(6, 24)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password1 = PasswordField("Password", validators=[DataRequired(), Length(12, 64)])
    password2 = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password1")]
    )
    recaptcha = RecaptchaField("Recaptcha", validators=[Recaptcha()])
    register = SubmitField("Register")


class YesNo(FlaskForm):
    """
    Form for Yes/No options.
    Parameters:
    - options: User's choice, either 'y' for Yes or 'n' for No
    """
    options = RadioField(choices=[("y", "Yes"), ("n", "No")])
    submit = SubmitField("Submit")
    theme_toggle = SubmitField("ThemeToggle")


class StreakForm(FlaskForm):
    """
    Form for managing habit streaks.
    Parameters:
    - hidden_id: Hidden field to store habit_id for internal use
    """
    hidden_id = HiddenField(name="habit_id")
    submit = SubmitField("Done")
    update = SubmitField("Update")
    delete = SubmitField("Delete")


class UpdateForm(FlaskForm):
    """
    Form for updating habit information.
    Parameters:
    - reason: Updated reason for wanting to do the habit
    - name: Updated name of the habit
    """
    reason = TextAreaField(
        name="updated_reason", validators=[DataRequired(), Length(8, 64)]
    )
    name = StringField(name="update_name", validators=[DataRequired(), Length(8, 64)])
    submit = SubmitField("Update")


class ShopForm(FlaskForm):
    """
    Form for shop actions.
    Parameters: None
    """
    theme_customization = SubmitField("Purchase Custom Theme")
    streak_freeze = SubmitField("Purchase Streak Freeze")


class ThemeForm(FlaskForm):
    """
    Form for customizing themes.
    Parameters:
    - primary_color: User's chosen primary color
    - secondary_color: User's chosen secondary color
    - accent_color: User's chosen accent color
    - background_color: User's chosen background color
    """
    primary_color = StringField(
        "Primary Color", widget=ColorInput(), validators=[DataRequired()]
    )
    secondary_color = StringField(
        "Secondary Color", widget=ColorInput(), validators=[DataRequired()]
    )
    accent_color = StringField(
        "Accent Color", widget=ColorInput(), validators=[DataRequired()]
    )
    background_color = StringField(
        "Background Color", widget=ColorInput(), validators=[DataRequired()]
    )
    submit = SubmitField("Submit")
