from datetime import datetime
from app import mail, db
import pytz
from flask_mail import Message
from flask import url_for, flash
from app.models import UserAchievements, Achievements

# Get local date for location
def get_local_date():
    # replace with your local timezone
    local_tz = pytz.timezone('Pacific/Auckland')
    return datetime.now(local_tz).date()

# Streak to see if two habits are consecutive in days
def check_consecutive(streak_parameter, user):
    previous_date = streak_parameter.date
    date = get_local_date()
    streak_total = streak_parameter.is_consecutive
    # Gets the total score which is the number of uninterrupted days of doing a day consecutive
    delta = date - previous_date
    if delta.days == 1:
        streak_total += 1
        if streak_total > user.longest_streak:
            user.longest_streak = streak_total
            db.session.commit()
        return streak_total
    else:
        return 1

# Function to convert data to suitable for heatmap in javascript
def heatmap_data(data):
    heatmap_data_list = []
    for i in data:
        date_str = str(i.date)
        streak_count = i.is_consecutive
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')  # Convert date string to date object
        day_of_week = date_obj.weekday()

        heatmap_data_list.append({
            'date': date_obj,         # Date string
            'week day': str(day_of_week),  # Convert day_of_week to string
            'date_string': date_obj,         # Date string
            'streak_count': streak_count      # Streak count
        })

    return heatmap_data_list

"""
Check data for multiple entries on the same days.
If there are then add 1 to the total number of habits done.
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
def habit_points(user_streak, type_of_habit, user):
    total_points = 100
    user.total_habits_tracked += 1
    db.session.commit()
    # Award different points for breaking bad habit. To encourage with incentives certain behavior
    if type_of_habit == 'bad':
        user.bad_habits_tracked += 1
        if user_streak:
            if user_streak <= 14:
                total_points += user_streak * 20
            else:
                total_points += user_streak * 10 + 14 * 20
    elif type_of_habit == 'good':
        user.good_habits_tracked += 1
        if user_streak:
            total_points += user_streak * 15
    return total_points

# function sends the user a verification email
def email_verification(user_email, token):
    msg = Message("Authentication link", recipients=[user_email])
    # send an email with the subject Authentication Link. Recipient will be what the user enters in the email field
    msg.body = ("This is your authentication link {}. \n Remember to log in with your defined username and password from registration.".format(url_for('authentication', token=token, _external=True)))
    # Includes a link to verify the account for the user
    return mail.send(msg)

def email_reminders(user_email, username):
    msg = Message('Habit Reminder', recipients=[user_email])
    msg.body = (" Hi {}, \n Reminder to make sure to log on to hadit and track your habits today".format(username))
    return mail.send(msg)

def streak_freezer(user_info):
    pass

