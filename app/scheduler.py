from apscheduler.schedulers.background import BackgroundScheduler
from app import Mail
import flask_mail
from app.models import users, habits, streak
scheduler=BackgroundScheduler()

def email_user():