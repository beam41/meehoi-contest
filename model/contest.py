from db import db


class Contest(db.Model):
    __tablename__ = 'contests'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, unique=True)
    index = db.Column(db.Integer, autoincrement=True)
