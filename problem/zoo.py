from typing import Union
from .base import Problem


class ZooProblem(Problem):
    @property
    def id(self) -> str:
        return "zoo"

    def evaluate(self, dataset: str, test_data: str) -> tuple[bool, Union[int, str]]:
        # TODO: Implement real evaluation
        dataset = self.load_dataset(dataset).strip().split("\n")

        try:
            test_data = test_data.strip().split("\n")

            if (len(test_data) != len(dataset)-1):
                return True, "Invalid: Number of test data is not equal to number of data in dataset"

            score = 0
            for i in range(1, int(dataset[0])+1):
                if test_data[i-1] == dataset[i]:
                    score += 1
            return False, score
        except Exception as e:
            return True, "Exception: " + str(e)
