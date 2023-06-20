from app import db
from datetime import datetime, timedelta  # import datetime modules
from flask_login import UserMixin  # import Usermixin class from flask_login
# import Check_password_hash and generate_password_hash from werkzeug.security
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy_utils import EncryptedType
from os import environ

encryption_key = environ.get('encryption_key')


class habits(db.Model):  # define 'habits' table
    __tablename__ = "habits"  # add 'habits' tablename
    # create primary key for habits table
    id = db.Column(db.Integer, primary_key=True)
    # create name column for table
    name = db.Column(EncryptedType(db.String(50), encryption_key))
    # create reason column for table
    reason = db.Column(EncryptedType(db.String(128), encryption_key))

    habit_type = db.Column(db.String(4))
    # create foreign key for user_id in user table
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # establish one to many relationship with users table
    user = db.relationship("users", secondary="streak",
                           backref="habits", overlaps="habits,user_streak")
    streak = db.relationship(
        'streak', backref='related_habits', overlaps="habits", cascade='delete,all')


class users(db.Model, UserMixin):  # define 'users' table and include UserMixin class
    __tablename__ = "users"  # add 'users' tablename
    # create primary key for user table stored as integer
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # column for usernames stored as string. With maximum length of 50.
    username = db.Column(EncryptedType(
        db.String(50), encryption_key), unique=True)
    # column for user password hash stored as string.
    password_hash = db.Column(db.String)
    # column for user email stored as string
    email = db.Column(EncryptedType(
        db.String(50), encryption_key), unique=True)
    # column for recording when user joined. Stored as datetime object. Defualt to current date.
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    email_notifactions = db.Column(
        db.Boolean, default=False)
    email_authentication = db.Column(
        db.Boolean, default=False)
    user_points = db.Column(db.Integer, default=0)

    def get_id(self):  # function that returns own id
        return self.id

    def set_password(self, password):  # function that generates password hash when called
        self.password_hash = generate_password_hash(password)

    # function that generates password hash when called
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # establish many to many relationship with 'streak' table
    streak = db.relationship(
        "habits", secondary="streak", backref="user_streak", overlaps="habits,streak,user,user_streak", cascade="delete,all")


class streak(db.Model):  # define 'streak' table
    __tablename__ = "streak"  # add 'streak' as tablename
    # create primary key for streak table. Stored as integer
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        "users.id"), nullable=False)  # Foreign key column for user id
    habit_id = db.Column(db.Integer, db.ForeignKey(
        "habits.id"), nullable=False)  # Foreign key column for habit id
    # column to record when habit is recorded. Stored as a datetime object. Defualts to current date.
    date = db.Column(
        db.Date, default=datetime.utcnow().date(), nullable=False)
    # column to record current streak for users habit
    is_consecutive = db.Column(db.Integer, default=0)
    # establish relationship with 'user' table
    user = db.relationship("users", backref="streaks")
    # establish relationship with 'habits' table
    habit = db.relationship("habits", backref="streaks",
                            overlaps="habits,user_streak,users")
    __table_args__ = (db.UniqueConstraint(
        'user_id', 'habit_id', 'date', name='_user_habit_date_uc'),)
