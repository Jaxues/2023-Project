from app import app
from apscheduler.schedulers.background import BackgroundScheduler
from functools import partial
from app.function import  email_reminders
from app.models import Users
# Setup scheduler
"""
with app.app_context():
    scheduler=BackgroundScheduler()
    email_users=Users.query.filter_by()
    for user in email_users:
        if user.email_notifactions:
            scheduler.add_job(partial(email_reminders, user.email, user.username),'cron', hour=8)
    scheduler.start()
""" 
if __name__ == '__main__':
    app.run(debug=True)