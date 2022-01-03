from database import db
from models.dataset import Dataset
from models.submission import Submission
from utils.gen_id import generate_sql_id


class Problem(db.Model):
    __tablename__ = 'problems'

    id: str = db.Column(db.String(10), primary_key=True,
                        default=generate_sql_id)
    name: str = db.Column(db.String, unique=True, nullable=False)
    index: int = db.Column(db.Integer, autoincrement=True, nullable=False)

    datasets: list[Dataset] = db.relationship(
        'Dataset', backref='problems', lazy=True)
    submissions: list[Submission] = db.relationship(
        'Submission', backref='problems', lazy=True)
