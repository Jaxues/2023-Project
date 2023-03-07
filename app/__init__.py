from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import environ
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///Hadit.db'
app.config['SECRET_KEY']=environ['secret_key']
db=SQLAlchemy(app)
from app import forms, models, routes
