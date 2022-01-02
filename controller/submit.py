from operator import itemgetter
from flask import request, Blueprint

from contest import get_contest

submit_controller = Blueprint('submit', __name__)


@submit_controller.route('/submit', methods=['POST'])
def submit():
    """
    Submit a new data to evaluate score and save to database.

    body:
        contest: Id of the contest
        dataset: dataset which the test data generated from
        test_data: test data
    """
    contest, dataset, test_data = itemgetter(
        'contest', 'dataset', 'testData')(request.get_json())

    load_contest = get_contest(contest)

    error, result = load_contest.evaluate(dataset, test_data)

    return {'error': error, 'result': result}
