from database import db
from models.dataset import Dataset
from models.submission import Submission


class Problem(db.Model):
    __tablename__ = 'problems'

    id: str = db.Column(db.String, primary_key=True)
    name: str = db.Column(db.String, unique=True, nullable=False)
    index: int = db.Column(db.Integer, autoincrement=True, nullable=False)

    datasets: list[Dataset] = db.relationship(
        'Dataset', backref='problems', lazy=True)
    submissions: list[Submission] = db.relationship(
        'Submission', backref='problems', lazy=True)
