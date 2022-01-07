from dataclasses import dataclass


@dataclass
class LeaderBoardScoreDto:
    id: str
    username: str
    score: int
    rank: int


@dataclass
class LeaderboardDto:
    ranks: list[LeaderBoardScoreDto]


def from_query_result(result: list[tuple]) -> LeaderboardDto:
    return LeaderboardDto([LeaderBoardScoreDto(id, username, score, rank) for id, username, score, rank in result])
