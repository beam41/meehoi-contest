from operator import itemgetter
from flask import request, Blueprint, current_app as app
from os import makedirs, path
from flask_jwt_extended import jwt_required
from flask_jwt_extended.utils import get_jwt_identity

from problems import get_problem
from repositories import submission


submit_controller = Blueprint('submit', __name__, url_prefix='/submit')


@submit_controller.route('', methods=['POST'])
@jwt_required()
def submit():
    """
    Generate new submission in the database before submit data and code.

    body:
        problem: Id of the problem
    """
    problem = itemgetter('problem')(request.get_json())
    user_id = get_jwt_identity()
    id = submission.add_submission(problem, user_id)
    return {'id': id}


@submit_controller.route('/data', methods=['POST'])
@jwt_required()
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
        'problem', 'dataset', 'test_data', 'submission_id')(request.json)
    user_id = get_jwt_identity()

    if not submission.check_submission_owner(submission_id, user_id):
        return {'msg': 'You are not the owner of this submission'}, 403

    loaded_problem = get_problem(problem)

    error, result = loaded_problem.evaluate(dataset, test_data)

    submission.update_score(submission_id, dataset, error,
                            result if error else None,
                            result if not error else None)

    return {'error': error, 'result': result}


@submit_controller.route('/code', methods=['POST'])
@jwt_required()
def submit_code():
    """Save source code to static and update path to database"""
    file = request.files['file']
    submission_id = request.form['submission_id']
    user_id = get_jwt_identity()

    if not submission.check_submission_owner(submission_id, user_id):
        return {'msg': 'You are not the owner of this submission'}, 403

    makedirs(path.join(app.static_folder, "submit", submission_id), exist_ok=True)
    file.save(path.join(app.static_folder, "submit",
              submission_id, file.filename))

    submission.update_codepath(
        submission_id,
        "/".join(["submit",
                  submission_id,
                  file.filename])
    )

    return {'completed': True}
