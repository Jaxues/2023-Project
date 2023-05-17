from datetime import datetime
import pytz
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


def heatmap_date_checker(data):
    days_done = {}
    for x in data:
        if x.date in days_done:
            days_done[x.date] += 1
        else:
            days_done[x.date] = 1
    return days_done
