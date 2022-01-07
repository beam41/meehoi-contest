from database import db
from datetime import datetime


class Leaderboard(db.Model):
    __tablename__ = 'leaderboard'

    user_id: str = db.Column(db.CHAR(5), db.ForeignKey(
        'users.id'), primary_key=True)
    problem_id: str = db.Column(db.String, db.ForeignKey(
        'problems.id'), primary_key=True)

    score: int = db.Column(db.Integer)
    best_time: datetime = db.Column(db.DateTime(timezone=True))
    rank: int = db.Column(db.Integer)
