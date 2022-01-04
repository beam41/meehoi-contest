from dataclasses import dataclass
from .score_dto import ScoreDto

@dataclass
class SubmissionWithScoreDto:
    id: str
    scores: list[ScoreDto]
