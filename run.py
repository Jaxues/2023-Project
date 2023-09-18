from app import app
from apscheduler.schedulers.background import BackgroundScheduler
from functools import partial
from app.function import  email_reminders
from app.models import Users

if __name__ == '__main__':
    app.run(debug=True)