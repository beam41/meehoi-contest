from database import db
from utils.gen_id import generate_sql_id


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(10), primary_key=True, default=generate_sql_id)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    submissions = db.relationship('Submission', backref='users', lazy=True)
