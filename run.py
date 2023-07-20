from app import app
from apscheduler.schedulers.background import BackgroundScheduler
from functools import partial
from app.function import award_achievement, email_reminders
from app.models import users
# Setup scheduler
with app.app_context():
    scheduler=BackgroundScheduler()
    total_users=users.query.all()
    for user in total_users:
        scheduler.add_job(partial(award_achievement,user), 'interval', hours=4)
        if user.email_notifactions:
            scheduler.add_job(partial(email_reminders, user.email),'cron', hour=8)
    scheduler.start()
if __name__ == '__main__':
    app.run(debug=True)