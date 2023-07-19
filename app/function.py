from datetime import datetime
from app import mail, db
import pytz
from flask_mail import Message
from flask import url_for
from flask import flash
from app.models import user_achievements, achievements

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
    # Award different points for breaking bad habit. To encourage with incentives certain behaviour
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

# function sends user a verification email
def email_verification(user_email, token):
    msg= Message("Authentication link", recipients=[user_email])
    # send an email with the subject Authentication Link. Recipetient will be what user enters in email field
    msg.body=("This is your authentication link {}. \n Remember to login in with your defined username and password from registration.".format(url_for('authentication', token=token, _external=True)))
    # Includes link to verify account for user
    return mail.send(msg)

def award_achievement(user_check):
    achievement_list = []
    achievements_total=achievements.query.all()
    for achievement in achievements_total:
        achievement_list.append({'id': achievement.id, 'requirements': achievement.requirements})
    
    for achievement in achievement_list:
        # Code for checking achievements for streaks
        if achievement['id'] < 4:
            if achievement['requirements'] == user_check.longest_streak:
                flash('success', 'You earned {} achievement for {}'.format(achievement.name, achievement.description))
                if user_achievements.query.filter_by(id=achievement['id']).first():
                    pass
                else:
                    new_user_achievement = user_achievements(achievement_id=achievement['id'], user_id=user_check.id)
                    db.session.add(new_user_achievement)
                    db.session.commit()
        # Code for checking achievements for Good Habits
        elif 3 < achievement['id'] < 7:
           if achievement['requirements'] == user_check.good_habits_tracked:
                flash('success', 'You earned {} achievement for {}'.format(achievement.name, achievement.description))
                if user_achievements.query.filter_by(id=achievement['id']).first():
                    pass
                else:
                    new_user_achievement = user_achievements(achievement_id=achievement['id'], user_id=user_check.id)
                    db.session.add(new_user_achievement)
                    db.session.commit()
    # Code for checking achievements for Breaking Bad Habits
        elif 6 < achievement['id'] < 10:
            if achievement['requirements'] == user_check.bad_habits_tracked:
                    flash('success', 'You earned {} achievement for {}'.format(achievement.name, achievement.description))
                    if user_achievements.query.filter_by(id=achievement['id']).first():
                        pass
                    else:
                        new_user_achievement = user_achievements(achievement_id=achievement['id'], user_id=user_check.id)
                        db.session.add(new_user_achievement)
                        db.session.commit()
        # Code for checking achievements for Total Habits Completed 
        elif 10 < achievement['id'] < 13: 
            if achievement['requirements'] == user_check.total_habits_complete:
                            flash('success', 'You earned {} achievement for {}'.format(achievement.name, achievement.description))
                            if user_achievements.query.filter_by(id=achievement['id']).first():
                                pass
                            else:
                                new_user_achievement = user_achievements(achievement_id=achievement['id'], user_id=user_check.id)
                                db.session.add(new_user_achievement)
                                db.session.commit()
        # Code for checking achievements for Completion habits 
        elif 14 < achievement['id'] < 19:
            if achievement['requirements'] == user_check.total_achievements:
                flash('success', 'You earned {} achievement for {}'.format(achievement.name, achievement.description))
                if user_achievements.query.filter_by(id=achievement['id']).first():
                    pass
                else:
                    new_user_achievement = user_achievements(achievement_id=achievement['id'], user_id=user_check.id)
                    db.session.add(new_user_achievement)
                    db.session.commit()
        # Code for checking achievements for getting point total 
        elif achievement['id']==19:
            if achievement['requirements'] == user_check.total_points:
                flash('success', 'You earned {} achievement for {}'.format(achievement.name, achievement.description))
                if user_achievements.query.filter_by(id=achievement['id']).first():
                    pass
                else:
                    print('Achievement not award this way.') 

def email_reminders(user_email):
    msg= Message('Habit Reminder',recipients={user_email})
    msg.body=("Reminder to make sure to log on to hadit and track your habits today")
    return mail.send(msg)