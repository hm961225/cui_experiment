from app.models import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, index=True, primary_key=True)
    username = db.Column(db.String(128), index=True, unique=True)
    password = db.Column(db.String(128))