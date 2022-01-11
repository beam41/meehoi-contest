from dataclasses import dataclass


@dataclass
class ScoreDto:
    dataset_id: str
    is_error: bool
    error_txt: str
    score: int
    is_running: bool
