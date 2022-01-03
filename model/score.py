from database import db


class Score(db.Model):
    __tablename__ = 'scores'

    submission_id = db.Column(db.String(10), db.ForeignKey(
        'submissions.id'), primary_key=True)
    dataset_id = db.Column(db.String(10), db.ForeignKey(
        'datasets.id'), primary_key=True)

    is_error = db.Column(db.Boolean, nullable=False)
    error_txt = db.Column(db.String, nullable=True)
    score = db.Column(db.Integer, nullable=False)
