from datetime import datetime
from app import mail
import pytz
from flask_mail import Message
from flask import url_for
from itsdangerous import URLSafeTimedSerializer
# Get local date for location

def get_local_date():
    # replace with your local timezone
    local_tz = pytz.timezone('Pacific/Auckland')
    return datetime.now(local_tz).date()

# Streak to see if two habits are consecutive in days


def check_consecutive(steak_paramter):
    previous_date = steak_paramter.date
    date = get_local_date()
    streak_total = steak_paramter.is_consecutive
    # Gets the total score which is the number of uninterupted days of doing a day consecutive
    delta = date - previous_date
    if delta.days == 1:
        return streak_total+1
    else:
        return 1

# Function to convert data to suitable for heatmap in javascript


def heatmap_data(data):
    heatmap_dict = []
    for i in data:
        # Iterate through all the data and add it as two values in a dictionary.
        date = i.date
        streak = i.is_consecutive
        heatmap_dict.append({'date': date, 'streak': streak})
    return heatmap_dict


"""
Check data for multiple entris on same days. 
If there are then add 1 to total number of habits done
"""


def heatmap_date_checker(data):
    days_done = {}
    for x in data:
        date_str = x['date'].strftime('%Y-%m-%d')
        if date_str in days_done:
            days_done[date_str] += 1
        else:
            days_done[date_str] = 1
    return days_done

# Define scoring for habits


def habit_points(user_streak, type_of_habit):
    total_points = 100
    if type_of_habit == 'bad':
        if user_streak:
            if user_streak <= 14:
                total_points += user_streak*20
            else:
                total_points += user_streak*10+140
    elif type_of_habit == 'good':
        if user_streak:
            total_points += user_streak*15
    return total_points

def email_verification(user_email, token):
    msg= Message("Authentication link", recipients=[user_email])
    msg.body=("This is your authentication link {}".format(url_for('authentication', token=token, _external=True)))
    return mail.send(msg)