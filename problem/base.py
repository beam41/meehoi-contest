from typing import Union
from flask import current_app as app
from os import path


class Problem:
    """Base class for problem."""

    @property
    def id(self) -> str:
        """Id of the problem. Must match with the name of the folder in static and database id."""
        pass

    def evaluate(self, dataset: str, test_data: str) -> tuple[bool, Union[int, str]]:
        """
        Evaluate the test data and return tuple (is_error, the int score or string if error).

        error string should be in format: `<type>: <message>`

        type:
        `Invalid`: Validation failed
        `Exception`: Exception occurred

        :param dataset: Id of dataset. In case the evaluate function need to load information from dataset.
        :param test_data: test data
        """
        pass

    def load_dataset(self, dataset: str) -> str:
        """
        Sometime we need to load dataset to get information not available in test data.

        This will load one from static folder.

        :param dataset: Id of dataset which is also the name of the file.
        """
        with open(path.join(app.static_folder, self.id, dataset + ".in")) as f:  # dataset always end with .in
            return f.read()
