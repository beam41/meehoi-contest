from database import db


class Problem(db.Model):
    __tablename__ = 'problems'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, unique=True)
    index = db.Column(db.Integer, autoincrement=True)
