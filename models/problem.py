from database import db
from models.dataset import Dataset
from models.submission import Submission
from .dto import ProblemWithIndexDto, ProblemWithDatasetDto


class Problem(db.Model):
    __tablename__ = 'problems'

    id: str = db.Column(db.String, primary_key=True)
    name: str = db.Column(db.String, unique=True, nullable=False)
    index: int = db.Column(db.Integer, nullable=False)

    datasets: list[Dataset] = db.relationship(
        'Dataset', backref='problems', lazy=True)
    submissions: list[Submission] = db.relationship(
        'Submission', backref='problems', lazy=True)

    def to_problem_with_index(self) -> ProblemWithIndexDto:
        return ProblemWithIndexDto(self.id, self.name, self.index)

    def to_problem_with_dataset(self) -> ProblemWithDatasetDto:
        return ProblemWithDatasetDto(self.id, self.name, [dataset.to_dataset_dto() for dataset in self.datasets])
