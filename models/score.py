from database import db
from .dto import ScoreDto


class Score(db.Model):
    __tablename__ = 'scores'

    submission_id: str = db.Column(db.CHAR(10), db.ForeignKey(
        'submissions.id'), primary_key=True)
    dataset_id: str = db.Column(db.String, db.ForeignKey(
        'datasets.id'), primary_key=True)

    is_error: bool = db.Column(db.Boolean, nullable=False)
    error_txt: str = db.Column(db.String, nullable=True)
    score: int = db.Column(db.Integer, nullable=True)

    def to_score_dto(self):
        return ScoreDto(
            self.dataset_id,
            self.is_error,
            self.error_txt,
            self.score
        )
