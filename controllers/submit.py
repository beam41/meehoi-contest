from operator import itemgetter
from flask import request, Blueprint, current_app as app
from os import makedirs, path

from problems import get_problem


submit_controller = Blueprint('submit', __name__, url_prefix='/submit')


@submit_controller.route('/', methods=['POST'])
def submit():
    """
    Generate new submission in the database before submit data and code.

    body:
        problem: Id of the problem
    """
    problem = itemgetter('problem')(request.get_json())
    # TODO: get user id from auth
    user_id = "asdads"
    # TODO: add submission row and return database id
    return "gyjhgj"


@submit_controller.route('/data', methods=['POST'])
def submit_data():
    """
    Submit a new data to evaluate score and save to database.

    body:
        problem: Id of the problem
        dataset: dataset which the test data generated from
        test_data: test data
        submission_id: Id of the submission.
    """
    problem, dataset, test_data, submission_id = itemgetter(
        'problem', 'dataset', 'testData', 'submissionId')(request.json)
    # TODO: get user id from auth
    user_id = "asdads"

    loaded_problem = get_problem(problem)

    error, result = loaded_problem.evaluate(dataset, test_data)

    # TODO: save to db

    return {'error': error, 'result': result}


@submit_controller.route('/code', methods=['POST'])
def submit_code():
    """Save source code to static and update path to database"""
    file = request.files['file']
    submission_id = request.form['submissionId']

    makedirs(path.join(app.static_folder, "submit", submission_id), exist_ok=True)
    file.save(path.join(app.static_folder, "submit",
              submission_id, file.filename))

    # TODO: save to db

    return {'error': False}
