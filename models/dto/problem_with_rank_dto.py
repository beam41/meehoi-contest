from dataclasses import dataclass


@dataclass
class ProblemWithRankDto:
    id: str
    name: str
    index: int
    rank: int
    
