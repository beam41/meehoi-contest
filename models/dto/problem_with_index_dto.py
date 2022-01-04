from dataclasses import dataclass


@dataclass
class ProblemWithIndexDto:
    id: str
    name: str
    index: int
