from operator import itemgetter
from flask import request, Blueprint, current_app as app
from os import makedirs, path
from werkzeug.datastructures import FileStorage

from contest import get_contest


submit_controller = Blueprint('submit', __name__)


@submit_controller.route('/submit', methods=['POST'])
def submit():
    """
    Generate new submission in the database before submit data and code.

    body:
        contest: Id of the contest
    """
    contest = itemgetter('contest')(request.get_json())
    # TODO: get user id from auth
    user_id = "asdads"
    # TODO: add submission row and return database id
    return "gyjhgj"


@submit_controller.route('/submit-data', methods=['POST'])
def submit_data():
    """
    Submit a new data to evaluate score and save to database.

    body:
        contest: Id of the contest
        dataset: dataset which the test data generated from
        test_data: test data
        submission_id: Id of the submission.
    """
    contest, dataset, test_data, submission_id = itemgetter(
        'contest', 'dataset', 'testData', 'submissionId')(request.json)
    # TODO: get user id from auth
    user_id = "asdads"

    load_contest = get_contest(contest)

    error, result = load_contest.evaluate(dataset, test_data)

    # save file to static folder
    makedirs(path.join(app.static_folder, "submit", submission_id), exist_ok=True)
    with open(path.join(app.static_folder, "submit", submission_id, dataset+".out"), "w") as f:
        f.write(test_data)

    # TODO: save to db

    return {'error': error, 'result': result}


@submit_controller.route('/submit-code', methods=['POST'])
def submit_code():
    """Save source code to static and update path to database"""
    file = request.files['file']
    submission_id = request.form['submissionId']

    makedirs(path.join(app.static_folder, "submit", submission_id), exist_ok=True)
    file.save(path.join(app.static_folder, "submit",
              submission_id, file.filename))

    # TODO: save to db

    return {'error': False}
