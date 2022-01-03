from database import db
from models.submission import Submission
from utils.gen_id import generate_user_id


class User(db.Model):
    __tablename__ = 'users'

    id: str = db.Column(db.String(5), primary_key=True,
                        default=generate_user_id)
    username: str = db.Column(db.String, nullable=False, unique=True)
    password: str = db.Column(db.String, nullable=False)

    submissions: list[Submission] = db.relationship(
        'Submission', backref='users', lazy=True)
