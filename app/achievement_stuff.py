from app import db
from app.models import Achievements


def add_achievements():
    # Check if achievements already exist in the database
    existing_achievements = Achievements.query.all()
    if not existing_achievements:
        # Create and add achievements to the database

        """
        Rarity of 1 is common, 2 is uncommon, 3 is rare, and 4 is miscenalous
        Requirements are numerical terms.
        For Purchase streak freeze, theme customization and account creation. True is stored as one.
        So checking this value works for reequirements

        Progression is measured in percentage of achievements completed.
        0.25 is 25%, 0.75 is 75%, etc.

        All other values for requirements are the number of occurences needed.
        For streak, break bad habit, and maintain good habit,
        theese are the number of days.

        For habit completion this is the total of all entries in the streaks table
        """

        achievement_data = [{'name': 'Bronze Streak', 'rarity': 1, 'category': 'Streak Award',
                             'description': 'Maintain a streak of 7 consecutive days', 'requirements': 7},
                            {'name': 'Silver Streak', 'rarity': 2, 'category': 'Streak Award',
                                'description': 'Maintain a streak of 14 consecutive days',
                                'requirements': 14},
                            {'name': 'Gold Streak', 'rarity': 3, 'category': 'Streak Award',
                                'description': 'Maintain a streak of 30 consecutive days',
                                'requirements': 30},
                            {'name': 'Bronze Habit', 'rarity': 1, 'category': 'Establish Good Habit',
                                'description': 'Maintain a habit for 7 consecutive days',
                                'requirements': 7},
                            {'name': 'Silver Habit', 'rarity': 2, 'category': 'Establish Good Habit',
                                'description': 'Maintain a habit for 14 consecutive days',
                                'requirements': 14},
                            {'name': 'Gold Habit', 'rarity': 3, 'category': 'Establish Good Habit',
                                'description': 'Maintain a habit for 30 consecutive days',
                                'requirements': 30},
                            {'name': 'Bronze Break', 'rarity': 1, 'category': 'Break Bad Habit',
                                'description': 'Successfully go 7 days without a bad habit',
                                'requirements': 7},
                            {'name': 'Silver Break', 'rarity': 2, 'category': 'Break Bad Habit',
                                'description': 'Successfully go 14 days without a bad habit',
                                'requirements': 14},
                            {'name': 'Gold Break', 'rarity': 3, 'category': 'Break Bad Habit',
                                'description': 'Successfully go 30 days without a bad habit',
                                'requirements': 30},
                            {'name': 'Bronze Habits', 'rarity': 1, 'category': 'Total Habits Completed',
                                'description': 'Track 10 entries of habits',
                                'requirements': 10},
                            {'name': 'Silver Habits', 'rarity': 2, 'category': 'Total Habits Completed',
                            'description': 'Traci 30 entries of habits',
                                'requirements': 30},
                            {'name': 'Gold Habits', 'rarity': 3, 'category': 'Total Habits Completed',
                                'description': 'Track 50 entries of habits',
                            'requirements': 50},
                            {'name': 'Customize Theme', 'rarity': 4, 'category': 'Custom Theme',
                                'description': 'Customize the theme',
                                'requirements': 1},
                            {'name': 'Streak Freeze', 'rarity': 4, 'category': 'Streak Freeze',
                                'description': 'Purchase a streak freeze item',
                                'requirements': 1},
                            {'name': 'Bronze Milestone', 'rarity': 1, 'category': 'Progression Milestones',
                                'description': 'Achieve 25% of total achievements (5 achievements)',
                                'requirements': 0.25},
                            {'name': 'Silver Milestone', 'rarity': 2, 'category': 'Progression Milestones',
                                'description': 'Achieve 50% of total achievements (10 achievements)',
                                'requirements': 0.5},
                            {'name': 'Gold Milestone', 'rarity': 3, 'category': 'Progression Milestones',
                             'description': 'Achieve 75% of total achievements (15 achievements)',
                                'requirements': 0.75},
                            {'name': 'Completion Milestone', 'rarity': 4, 'category': 'Progression Milestones',
                                'description': 'Achieve 100% of total achievements (all 20 achievements)',
                                'requirements': 1},
                            {'name': 'Diamond Points', 'rarity': 4, 'category': 'Total Points Earned',
                                'description': 'Accumulate a total of 10,000 points',
                                'requirements': 1e4},
                            {'name': 'Account Creation', 'rarity': 4, 'category': 'Account',
                             'description': 'Create an account',
                             'requirements': 1}]
        # If table is emtpy prepopulate with achievements.
        for data in achievement_data:
            achievement = Achievements(**data)
            db.session.add(achievement)
            db.session.commit()
        print("Achievements added to the database.")
    else:
        print("Achievements already exist in the database.")
