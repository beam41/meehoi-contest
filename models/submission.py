from sqlalchemy.sql import func
from database import db
from models.score import Score
from utils.gen_id import generate_sql_id
from datetime import datetime

class Submission(db.Model):
    __tablename__ = 'submissions'

    id: str = db.Column(db.String(10), primary_key=True, default=generate_sql_id)
    code_path: str = db.Column(db.String)
    created_date: datetime = db.Column(db.DateTime(timezone=True), server_default=func.utcnow())

    problem_id: str = db.Column(db.String(10), db.ForeignKey(
        'problems.id'), nullable=False)
    user_id: str = db.Column(db.String(10), db.ForeignKey(
        'users.id'), nullable=False)

    scores: list[Score] = db.relationship('Score', lazy=True)
