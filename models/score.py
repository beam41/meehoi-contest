from database import db


class Score(db.Model):
    __tablename__ = 'scores'

    submission_id: str = db.Column(db.String(10), db.ForeignKey(
        'submissions.id'), primary_key=True)
    dataset_id: str = db.Column(db.String(10), db.ForeignKey(
        'datasets.id'), primary_key=True)

    is_error: bool = db.Column(db.Boolean, nullable=False)
    error_txt: str = db.Column(db.String, nullable=True)
    score: int = db.Column(db.Integer, nullable=False)
