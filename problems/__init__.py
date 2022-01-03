from .base import Problem
from .zoo import ZooProblem


problem_list: dict[str, Problem] = {
    problem.id: problem for problem in [
        ZooProblem()  # new problem here
    ]
}


def get_problem(id: str) -> Problem:
    if (id in problem_list):
        return problem_list[id]
