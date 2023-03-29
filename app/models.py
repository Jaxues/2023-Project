from app import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

"""
This module contains Flask SQLAlchemy models for the application.

Classes:
- habits: SQLAlchemy model for the habits table.
- users: SQLAlchemy model for the users table, using the UserMixin for authentication.

Attributes:
- id: Integer primary key for both tables.
- name: String column for habits table.
- userid: Integer foreign key referencing id column in users table.
- user: Relationship between habits and users table.
- username: String column for username in users table, must be unique.
- password_hash: String column for storing hashed passwords in users table.
- email: String column for email in users table, must be unique.
- date_joined: DateTime column for storing date and time of user registration in users table.

Methods:
- get_id(): Returns the id of the user for Flask-Login authentication.
- set_password(password): Hashes the provided password and stores it in the password_hash column.
- check_password(password): Checks if the provided password matches the hashed password stored in the password_hash column.
"""


class habits(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String)
    userid=db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user=db.relationship('users',backref='habits')

class users(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    username=db.Column(db.String, unique=True)
    password_hash=db.Column(db.String)
    email=db.Column(db.String, unique=True)
    date_joined=db.Column(db.DateTime, default=datetime.utcnow)
    def get_id(self):
        return self.id

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)