from app import app
from app.models import streak
from datetime import datetime, timedelta


def consective_streak(user_id, habit_id, date):
    streaks = streak.query().filter_by(
        user_id=user_id, habit_id=habit_id).order_by(streak.date.asc()).all()
    i = 1
    for entry in streaks:
        print(streaks[i], streak[i+1])


def test_function():
    return 'Hello World'
