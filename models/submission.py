from database import db
from models.dto import SubmissionWithScoreDto, SubmissionDto
from models.score import Score
from utils.gen_id import generate_submission_id
from datetime import datetime


class Submission(db.Model):
    __tablename__ = 'submissions'

    id: str = db.Column(db.String(10), primary_key=True,
                        default=generate_submission_id)
    code_path: str = db.Column(db.String)
    # TODO: switch to server_default=func.utcnow() after switching to other db engine
    created_date: datetime = db.Column(db.DateTime(
        timezone=True), default=datetime.utcnow)

    problem_id: str = db.Column(db.String, db.ForeignKey(
        'problems.id'), nullable=False)
    user_id: str = db.Column(db.String(5), db.ForeignKey(
        'users.id'), nullable=False)

    scores: list[Score] = db.relationship('Score', lazy=True)

    def to_submission_with_score_dto(self):
        return SubmissionWithScoreDto(
            self.id,
            [score.to_score_dto() for score in self.scores]
        )

    def to_submission_dto(self):
        return SubmissionDto(
            self.id,
            self.code_path,
            self.created_date.isoformat()
        )
