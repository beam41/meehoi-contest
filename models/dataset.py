from database import db
from utils.gen_id import generate_sql_id


class Dataset(db.Model):
    __tablename__ = 'datasets'

    id = db.Column(db.String(10), primary_key=True, default=generate_sql_id)
    name = db.Column(db.String, nullable=False)
    problem_id = db.Column(db.String(10), db.ForeignKey(
        'problems.id'), nullable=False)

    scores = db.relationship('Score', lazy=True)
