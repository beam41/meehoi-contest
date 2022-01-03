from database import db
from utils.gen_id import generate_sql_id


class Submission(db.Model):
    __tablename__ = 'submissions'

    id = db.Column(db.String(10), primary_key=True, default=generate_sql_id)
    code_path = db.Column(db.String)
    created_date = db.Column(db.DateTime)

    problem_id = db.Column(db.String(10), db.ForeignKey(
        'problems.id'), nullable=False)
    user_id = db.Column(db.String(10), db.ForeignKey(
        'users.id'), nullable=False)

    scores = db.relationship('Score', lazy=True)
