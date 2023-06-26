# neccesary imports for forms classes and dunctions
from flask_wtf import FlaskForm, Recaptcha, RecaptchaField
from wtforms.validators import DataRequired, Email, EqualTo, Length 
from wtforms import (
    StringField,
    SubmitField,
    PasswordField,
    TextAreaField,
    RadioField,
    HiddenField,
)
from wtforms.widgets import ColorInput
from wtforms import ValidationError
"""
Form for creating habits
Takes paramters of name which is the anme of the habit
The type of habit whether it is good or bad, Used with points function
Reason is text area field for why users wants to do habit
"""

class HabitForm(FlaskForm):
    name = StringField("name", validators=[DataRequired(), Length(5,50)])
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
    options = RadioField(choices=[('y','Yes'), ('n','No')])
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
    name= StringField(name='update name', validators=[DataRequired(), Length(8,64)])
    submit = SubmitField('update')

class ShopForm(FlaskForm):
    theme_customization= SubmitField('Purchase Custom Theme')
    streak_freeze=SubmitField('Purchase Streak Freeze')

class ThemeForm(FlaskForm):
    primary_color = StringField('Primary Color', widget=ColorInput(), validators=[DataRequired()])
    secondary_color = StringField('Secondary Color', widget=ColorInput(), validators=[DataRequired()])
    accent_color = StringField('Accent Color', widget=ColorInput(), validators=[DataRequired()])
    background_color = StringField('Background Color', widget=ColorInput(), validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate(self):
        if not super().validate():
            return False

        color_fields = [
            self.primary_color.data.lower(),
            self.secondary_color.data.lower(),
            self.accent_color.data.lower(),
            self.background_color.data.lower()
        ]
        if len(color_fields) != len(set(color_fields)):
            self.primary_color.errors.append('Colors must be unique.')
            return False

        return True