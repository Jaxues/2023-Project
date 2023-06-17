from apscheduler.schedulers.background import BackgroundScheduler
from app import Mail
from app.models import users, habits, streak
scheduler=BackgroundScheduler()

def email_user():