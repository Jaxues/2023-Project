from datetime import datetime
from app import mail, db
import pytz
from flask_mail import Message
from flask import url_for


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


def heatmap_converter(user_data):
    # Initialize a dictionary to aggregate data
    aggregated_data = {}
    # Iterate through user data
    for entry in user_data:
        date = entry.date

        if date in aggregated_data:
            # Increment count if the date is already in the dictionary
            aggregated_data[date]["v"] += 1
        else:
            # Create a new entry if the date is not in the dictionary
            day_of_week = date.weekday() + 1  # 1 for Monday, 2 for Tuesday
            aggregated_data[date] = {
                "x": date.isoformat(),
                "y": day_of_week,
                "d": date.isoformat(),
                "v": 1,  # Initial count
            }

    # Convert the values of the aggregated_data dictionary into a list
    final_user_data = list(aggregated_data.values())

    # Return the final user data as a list
    return final_user_data


# Define scoring for habits
def habit_points(user_streak, type_of_habit, user):
    total_points = 100
    user.total_habits_tracked += 1
    db.session.commit()
    # Award different points for breaking bad habit.
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
    # send an email with the subject Authentication Link.
    msg.body = ("This is your authentication link {}. \n Remember to log in with your defined username and password from registration.".format(url_for('authentication', token=token, _external=True)))
    # Includes a link to verify the account for the user
    return mail.send(msg)


def email_reminders(user_email, username):
    msg = Message('Habit Reminder', recipients=[user_email])
    msg.body = (" Hi {}, \n Reminder to make sure to log on to hadit and track your habits today".format(username))
    return mail.send(msg)


def streak_freezer(user_info):
    pass
