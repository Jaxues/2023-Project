from app import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
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
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)