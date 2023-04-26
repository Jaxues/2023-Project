from app import app
from flask_wtf import FlaskForm, Recaptcha,RecaptchaField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from wtforms import StringField, SubmitField, PasswordField, BooleanField,TextAreaField, RadioField
class HabitForm(FlaskForm):
    name=StringField('name',validators=[DataRequired()])
    reason=TextAreaField('reason')
    submit=SubmitField('submit')
class LoginForm(FlaskForm):
    username=StringField('username', validators=[DataRequired()])
    password=PasswordField('password', validators=[DataRequired()])
    submit=SubmitField('submit')

class RegisterForm(FlaskForm):
    username=StringField('username',validators=[DataRequired()])
    email=StringField('email', validators=[DataRequired(), Email()])
    password1=PasswordField('Password', validators=[DataRequired()])
    password2=PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password1')])
    recaptcha=RecaptchaField('Recaptcha',validators=[Recaptcha()])
    register=SubmitField('register')


class YesNo(FlaskForm):
    options=RadioField(choices=(['y','Yes'],['n','No']))
    submit=SubmitField('Submit')
