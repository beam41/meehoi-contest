from operator import itemgetter
from flask import request, Blueprint

submit_controller = Blueprint('submit', __name__)


@submit_controller.route('/submit', methods=['POST'])
def submit():
    """
    Submit a new data to evaluate score and save to database.

    body:
        contest: Id of the contest
        dataset: dataset which the test data generated from
        testData: test data
    """
    contest, dataset, test_data = itemgetter(
        'contest', 'dataset', 'testData')(request.get_json())
    return request.get_json(), 200
