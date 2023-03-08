from app import app
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField, PasswordField
class habitform(FlaskForm):
    name=StringField('name',validators=[DataRequired()])
    submit=SubmitField('submit')
class loginform(FlaskForm):
    username=StringField('username', validators=[DataRequired()])
    password=PasswordField('password', validators=[DataRequired()])
    submit=SubmitField('submit')