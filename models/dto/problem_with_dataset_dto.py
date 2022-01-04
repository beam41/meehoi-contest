from dataclasses import dataclass

from .dataset_dto import DatasetDto


@dataclass
class ProblemWithDatasetDto:
    id: str
    name: str
    datasets: list[DatasetDto]
