from dataclasses import dataclass


@dataclass
class LeaderBoardScoreDto:
    id: str
    username: str
    score: int


@dataclass
class LeaderboardDto:
    scores: list[LeaderBoardScoreDto]


def from_query_result(result: tuple[str, int]) -> LeaderboardDto:
    return LeaderboardDto([LeaderBoardScoreDto(id, username, score) for id, username, score in result])
