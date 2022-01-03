from database import db
from utils.gen_id import generate_sql_id


class Problem(db.Model):
    __tablename__ = 'problems'

    id = db.Column(db.String(10), primary_key=True, default=generate_sql_id)
    name = db.Column(db.String, unique=True, nullable=False)
    index = db.Column(db.Integer, autoincrement=True, nullable=False)

    datasets = db.relationship('Dataset', backref='problems', lazy=True)
    submissions = db.relationship('Submission', backref='problems', lazy=True)
