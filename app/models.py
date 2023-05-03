from app import db # import database object
from datetime import datetime # import datetime modules
from flask_login import UserMixin # import Usermixin class from flask_login
from werkzeug.security import check_password_hash, generate_password_hash # import Check_password_hash and generate_password_hash from werkzeug.security 

 
class habits(db.Model): # define 'habits' table
    __tablename__ = "habits" # add 'habits' tablename
    id = db.Column(db.Integer, primary_key=True) # create primary key for habits table
    name = db.Column(db.String(50)) # create name column for table
    reason = db.Column(db.String(128)) # create reason column for table
    user_id = db.Column(db.Integer, db.ForeignKey("users.id")) # create foreign key for user_id in user table 
    users = db.relationship("users", secondary="streak", backref="habits") # establish one to many relationship with users table


class users(db.Model, UserMixin): # define 'users' table and include UserMixin class
    __tablename__ = "users" # add 'users' tablename
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) # create primary key for user table stored as integer
    username = db.Column(db.String(50), unique=True) # column for usernames stored as string. With maximum length of 50. 
    password_hash = db.Column(db.String) # column for user password hash stored as string.
    email = db.Column(db.String, unique=True) # column for user email stored as string
    date_joined = db.Column(db.DateTime, default=datetime.utcnow) # column for recording when user joined. Stored as datetime object. Defualt to current date. 
    email_notifactions=db.Column(db.Boolean, default=False, name='email_notifactions')
    def get_id(self): # function that returns own id
        return self.id

    def set_password(self, password): # function that generates password hash when called
        self.password_hash = generate_password_hash(password)

    def check_password(self, password): # function that generates password hash when called
        return check_password_hash(self.password_hash, password)

    streak = db.relationship("habits", secondary="streak", backref="user_streak") # establish many to many relationship with 'streak' table


class streak(db.Model): # define 'streak' table
    __tablename__ = "streak" # add 'streak' as tablename
    id = db.Column(db.Integer, primary_key=True) # create primary key for streak table. Stored as integer
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False) # Foreign key column for user id
    habit_id = db.Column(db.Integer, db.ForeignKey("habits.id"), nullable=False) # Foreign key column for habit id
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False) # column to record when habit is recorded. Stored as a datetime object. Defualts to current date. 
    is_consecutive = db.Column(db.Integer, default=False) # column to record current streak for users habit
    user = db.relationship("users", backref="streaks") # establish relationship with 'user' table
    habit = db.relationship("habits", backref="streaks")  # establish relationship with 'habits' table

