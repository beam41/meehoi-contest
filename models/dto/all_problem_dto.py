from dataclasses import dataclass

from .problem_with_index_dto import ProblemWithIndexDto


@dataclass
class AllProblemDto:
    problems: list[ProblemWithIndexDto]
