from cryptography import fernet
from datetime import datetime, timedelta
from app.models import streak
import pytz


def get_local_date():
    # replace with your local timezone
    local_tz = pytz.timezone('Pacific/Auckland')
    return datetime.now(local_tz).date()


def check_consecutive(steak_paramter):
    previous_date = steak_paramter.date
    date = get_local_date()
    streak_total = steak_paramter.is_consecutive
    delta = date - previous_date
    if delta.days == 1:
        return streak_total+1
    else:
        return 1


print(get_local_date())
