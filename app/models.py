from app import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy_utils import EncryptedType
from os import environ

encryption_key = environ.get('encryption_key')


class Habits(db.Model):
    __tablename__ = "habits"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(EncryptedType(db.String(50), encryption_key))
    reason = db.Column(EncryptedType(db.String(128), encryption_key))
    habit_type = db.Column(db.String(4))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("Users", secondary="streak",
                           backref="habits", overlaps="habits,user_streak")
    streak = db.relationship(
        'Streak', backref='related_habits', overlaps="habits", cascade='delete,all')


class Users(db.Model, UserMixin):
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

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    theme = db.relationship('UserTheme', backref='user', uselist=False)
    streak = db.relationship(
        "Habits", secondary="streak", backref="user_streak", overlaps="habits,streak,user,user_streak", cascade="delete,all")
    user_achievements_rel = db.relationship('UserAchievements', backref='user')

    longest_streak = db.Column(db.Integer, default=0)
    bad_habits_tracked = db.Column(db.Integer, default=0)
    good_habits_tracked = db.Column(db.Integer, default=0)
    total_habits_tracked = db.Column(db.Integer, default=0)
    total_achievements = db.Column(db.Integer, default=0)
    total_points = db.Column(db.Integer, default=0)


class Streak(db.Model):
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
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    primary = db.Column(db.String, nullable=False)
    secondary = db.Column(db.String, nullable=False)
    accent = db.Column(db.String, nullable=False)
    background = db.Column(db.String, nullable=False)


class Achievements(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    rarity = db.Column(db.Integer)
    category = db.Column(db.String)
    description = db.Column(db.String)
    requirements = db.Column(db.Integer)
    achievements_rel = db.relationship('UserAchievements', backref='achievements')


class UserAchievements(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    achievement_id = db.Column(db.Integer, db.ForeignKey('achievements.id'), nullable=False)
    achievement = db.relationship('Achievements', backref="user_achievements")
