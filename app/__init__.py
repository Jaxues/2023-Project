from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail

app = Flask(__name__)
# Set up Database.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Hadit.db'
app.config['SECRET_KEY'] = environ['secret_key']
# Import secret key from enviorment variable for security
db = SQLAlchemy(app)
# Imports for Recapctha fields
app.config['RECAPTCHA_PUBLIC_KEY'] = environ['recap_pub']
app.config['RECAPTCHA_PRIVATE_KEY'] = environ['recap_priv']
# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
# Setup flask-mail
mail = Mail(app)
migrate = Migrate(app, db)
app.config['TESTING'] = bool(int(environ.get('testing_status',0)))
app.config['DEBUG']=app.config['TESTING']
from app import forms, models, routes