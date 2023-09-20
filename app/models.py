from app import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy_utils import EncryptedType
from os import environ

encryption_key = environ.get('encryption_key')


class Habits(db.Model):
    """
    id identifier for what habit is.
    name What the name of the habit
    reason Why user does habit
    habit_type Type of habit to break or build
    user_id Who habit belongs to
    """
    __tablename__ = "habits"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(EncryptedType(db.String(50), encryption_key))
    reason = db.Column(EncryptedType(db.String(128), encryption_key))
    habit_type = db.Column(db.String(4))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # Connect habit to user with one to many
    user = db.relationship("Users", secondary="streak",
                           backref="habits", overlaps="habits,user_streak")
    # Establish many to many with streak
    streak = db.relationship('Streak', backref='related_habits',
                             overlaps="habits", cascade='delete,all')


class Users(db.Model, UserMixin):
    """
    Table for storing all information for users
    Columns
    id: Unique identifer for which user is which.
    Unique and is used as a foriegn key in other
    username: What the user logins in with.
    password_hash: hashed verion of what the users password
    email: Where all notifactions as well as links will be sent to.
    email_notifactions: Whether or not a user wants notifactions
    email_authenticated: Neccesary to protect users account so that no one can use anothers email
    streak_freeze: Whether or not a user has a streak freeze powerup active.
    custom_theme: Whether or not a user has custom theme enabled within the website.
    """

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(EncryptedType(
        db.String(50), encryption_key), unique=True)
    password_hash = db.Column(db.String)
    email = db.Column(EncryptedType(
        db.String(50), encryption_key), unique=True)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    email_notifactions = db.Column(db.Boolean, default=False)
    email_authentication = db.Column(db.Boolean, default=False)
    user_points = db.Column(db.Integer, default=0)
    streak_freeze = db.Column(db.Boolean, default=False)
    custom_theme = db.Column(db.Boolean, default=False)

    def get_id(self):
        return self.id
    # Generate password hash

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # See if password entered is correct

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    # Establish theme to user one to one
    theme = db.relationship('UserTheme', backref='user', uselist=False)
    # Establish streak many to many
    streak = db.relationship(
        "Habits", secondary="streak", backref="user_streak",
        overlaps="habits,streak,user,user_streak", cascade="delete,all")
    user_achievements_rel = db.relationship('UserAchievements', backref='user')
    # Code realting to tracker user progress towards achievements over time

    longest_streak = db.Column(db.Integer, default=0)
    bad_habits_tracked = db.Column(db.Integer, default=0)
    good_habits_tracked = db.Column(db.Integer, default=0)
    total_habits_tracked = db.Column(db.Integer, default=0)
    total_achievements = db.Column(db.Integer, default=0)
    total_points = db.Column(db.Integer, default=0)


class Streak(db.Model):
    """
    Table for storing all data related to tracking the habits users have done on certain days
    Columns
    id Identifier of record
    user_id Who streak is for
    habit_id Which habit it is
    date What date recorded was done
    is_consecutive See if multiple days
    """
    __tablename__ = "streak"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        "users.id"), nullable=False)
    habit_id = db.Column(db.Integer, db.ForeignKey(
        "habits.id"), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow().date(), nullable=False)
    is_consecutive = db.Column(db.Integer, default=0)
    user = db.relationship("Users", backref="streaks")
    habit = db.relationship("Habits", backref="streaks",
                            overlaps="habits,user_streak,users")
    __table_args__ = (db.UniqueConstraint(
        'user_id', 'habit_id', 'date', name='_user_habit_date_uc'),)


class UserTheme(db.Model):
    """
    Table
    Column
    id Identifier for theme
    user_id Who theme belongs to
    primary What should be used for primary Color
    secondary What should be used for secondary Color
    accent What should be used for accent
    background What should be sued for background
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    primary = db.Column(db.String, nullable=False)
    secondary = db.Column(db.String, nullable=False)
    accent = db.Column(db.String, nullable=False)
    background = db.Column(db.String, nullable=False)


class Achievements(db.Model):
    """
    Storing all information relating to achievements.
    Including the name description, rarity and category and requirements.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    rarity = db.Column(db.Integer)
    category = db.Column(db.String)
    description = db.Column(db.String)
    requirements = db.Column(db.Integer)
    achievements_rel = db.relationship('UserAchievements',
                                       backref='achievements')


class UserAchievements(db.Model):
    """
    Table for storing data relating to achievments users have completed
    Columns:
    id: Unique identifier for the table. Need to order table. Primary Key
    user_id: Identifier of which user has achieved something.
    To be specific how has accomplished a certain achievement
    achievement_id: Which Achievement the user has accomplished.
    Theese are from the achievements table.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    achievement_id = db.Column(db.Integer,
                               db.ForeignKey('achievements.id'),
                               nullable=False)
    achievement = db.relationship('Achievements', backref="user_achievements")
