from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_login import LoginManager
from flask_migrate import Migrate
app=Flask(__name__)


# Set up Database. 
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///Hadit.db'
app.config['SECRET_KEY']=environ['secret_key']
db=SQLAlchemy(app)
migrate= Migrate(app, db)
# Imports for Recapctha fields
app.config['RECAPTCHA_PUBLIC_KEY']=environ['recap_pub']
app.config['RECAPTCHA_PRIVATE_KEY']=environ['recap_priv']

# Login Manager
login_manager=LoginManager()
login_manager.init_app(app)

app.config['TESTING']=environ['TESTING_STATUS']
from app import forms, models, routes
