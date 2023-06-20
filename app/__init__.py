from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_login import LoginManager
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
# Configure your Flask application
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = environ['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = environ['MAIL_PASSWORD']
app.config['MAIL_DEFAULT_SENDER'] = environ['MAIL_USERNAME']

mail = Mail(app)
from app import forms, models, routes
