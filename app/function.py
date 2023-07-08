from datetime import datetime
from app import mail, db
import pytz
from flask_mail import Message
from flask import url_for
from app.models import achievements

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

def add_achievements():
    # Check if achievements already exist in the database
    existing_achievements = achievements.query.all()
    
    if not existing_achievements:
        # Create and add achievements to the database
        achievement_data = [
            {'name': 'Bronze Streak', 'rarity': 1, 'category': 'Streak Award',
             'description': 'Maintain a streak of 7 consecutive days',
             'requirements': ''},
            {'name': 'Silver Streak', 'rarity': 2, 'category': 'Streak Award',
             'description': 'Maintain a streak of 30 consecutive days',
             'requirements': ''},
            {'name': 'Gold Streak', 'rarity': 3, 'category': 'Streak Award',
             'description': 'Maintain a streak of 90 consecutive days',
             'requirements': ''},
            {'name': 'Bronze Habit', 'rarity': 1, 'category': 'Establish Good Habit',
             'description': 'Maintain a habit for 7 consecutive days',
             'requirements': ''},
            {'name': 'Silver Habit', 'rarity': 2, 'category': 'Establish Good Habit',
             'description': 'Maintain a habit for 30 consecutive days',
             'requirements': ''},
            {'name': 'Gold Habit', 'rarity': 3, 'category': 'Establish Good Habit',
             'description': 'Maintain a habit for 90 consecutive days',
             'requirements': ''},
            {'name': 'Bronze Break', 'rarity': 1, 'category': 'Break Bad Habit',
             'description': 'Successfully go 7 days without a bad habit',
             'requirements': ''},
            {'name': 'Silver Break', 'rarity': 2, 'category': 'Break Bad Habit',
             'description': 'Successfully go 30 days without a bad habit',
             'requirements': ''},
            {'name': 'Gold Break', 'rarity': 3, 'category': 'Break Bad Habit',
             'description': 'Successfully go 90 days without a bad habit',
             'requirements': ''},
            {'name': 'Bronze Habits', 'rarity': 1, 'category': 'Total Habits Completed',
             'description': 'Complete 10 different habits',
             'requirements': ''},
            {'name': 'Silver Habits', 'rarity': 2, 'category': 'Total Habits Completed',
             'description': 'Complete 30 different habits',
             'requirements': ''},
            {'name': 'Gold Habits', 'rarity': 3, 'category': 'Total Habits Completed',
             'description': 'Complete 50 different habits',
             'requirements': ''},
            {'name': 'Customize Theme', 'rarity': 1, 'category': 'Custom Theme',
             'description': 'Customize the theme',
             'requirements': ''},
            {'name': 'Streak Freeze', 'rarity': 1, 'category': 'Streak Freeze',
             'description': 'Purchase a streak freeze item',
             'requirements': ''},
            {'name': 'Bronze Milestone', 'rarity': 1, 'category': 'Progression Milestones',
             'description': 'Achieve 25% of total achievements (5 achievements)',
             'requirements': ''},
            {'name': 'Silver Milestone', 'rarity': 2, 'category': 'Progression Milestones',
             'description': 'Achieve 50% of total achievements (10 achievements)',
             'requirements': ''},
            {'name': 'Gold Milestone', 'rarity': 3, 'category': 'Progression Milestones',
             'description': 'Achieve 75% of total achievements (15 achievements)',
             'requirements': ''},
            {'name': 'Platinum Milestone', 'rarity': 4, 'category': 'Progression Milestones',
             'description': 'Achieve 100% of total achievements (all 20 achievements)',
             'requirements': ''},
            {'name': 'Diamond Points', 'rarity': 4, 'category': 'Total Points Earned',
             'description': 'Accumulate a total of 10,000 points',
             'requirements': ''}
        ]
        
        for data in achievement_data:
            achievement = achievements(**data)
            db.session.add(achievement)
        
        db.session.commit()
        print("Achievements added to the database.")
    else:
        print("Achievements already exist in the database.")
