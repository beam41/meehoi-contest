from dataclasses import dataclass


@dataclass
class DatasetScoreDto:
    dataset_id: str
    score: int


@dataclass
class BestScoreDto:
    scores: DatasetScoreDto


def from_query_result(result: list[tuple]) -> BestScoreDto:
    return BestScoreDto([DatasetScoreDto(dataset_id, score) for dataset_id, score in result])
