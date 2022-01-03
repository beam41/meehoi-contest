from database import db
from models.score import Score
from utils.gen_id import generate_sql_id


class Dataset(db.Model):
    __tablename__ = 'datasets'

    id: str = db.Column(db.String, primary_key=True)
    name: str = db.Column(db.String, nullable=False)
    problem_id: str = db.Column(db.String(10), db.ForeignKey(
        'problems.id'), nullable=False)

    scores: list[Score] = db.relationship('Score', lazy=True)
