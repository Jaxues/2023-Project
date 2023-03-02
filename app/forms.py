from app import app
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField
class habitform(FlaskForm):
    name=StringField('name',validators=[DataRequired()])
    submit=SubmitField('submit')
