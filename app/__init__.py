from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_login import LoginManager
app=Flask(__name__)


# Set up Database. 
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///Hadit.db'
app.config['SECRET_KEY']=environ['secret_key']
db=SQLAlchemy(app)



# Login Manager
Login_manager=LoginManager()
login_manager=LoginManager()
login_manager.init_app(app)

from app import forms, models, routes
