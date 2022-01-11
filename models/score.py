from database import db
from .dto import ScoreDto
from sqlalchemy.sql.expression import true

class Score(db.Model):
    __tablename__ = 'scores'

    submission_id: str = db.Column(db.CHAR(10), db.ForeignKey(
        'submissions.id'), primary_key=True)
    dataset_id: str = db.Column(db.String, db.ForeignKey(
        'datasets.id'), primary_key=True)

    is_running: bool = db.Column(db.Boolean, nullable=False, server_default=true())
    is_error: bool = db.Column(db.Boolean, nullable=True)
    score: int = db.Column(db.Integer, nullable=True)
    error_txt: str = db.Column(db.String, nullable=True)

    def to_score_dto(self):
        return ScoreDto(
            self.dataset_id,
            self.is_error,
            self.error_txt,
            self.score,
            self.is_running
        )
