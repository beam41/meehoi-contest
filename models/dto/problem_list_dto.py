from dataclasses import dataclass

from .problem_with_rank_dto import ProblemWithRankDto


@dataclass
class ProblemListDto:
    problems: list[ProblemWithRankDto]


def from_query_result(result) -> ProblemListDto:
    return ProblemListDto([ProblemWithRankDto(id, name, index, rank) for id, name, index, rank in result])
