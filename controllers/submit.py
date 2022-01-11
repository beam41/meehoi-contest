from operator import itemgetter
from flask import request, Blueprint, current_app as app
from os import makedirs, path
from flask.json import jsonify
from flask_jwt_extended import jwt_required
from flask_jwt_extended.utils import get_jwt_identity
import asyncio

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
    file = request.files['file']
    problem = request.form['problem']
    user_id = get_jwt_identity()

    submission_ = submission.add_submission(
        problem,
        user_id,
        file.filename
    )

    makedirs(path.join(app.static_folder, "submit",
             submission_.id), exist_ok=True)
    file.save(path.join(app.static_folder, "submit",
              submission_.id, file.filename))

    return jsonify(submission_.to_submission_dto())


@submit_controller.route('/data', methods=['POST'])
@jwt_required()
async def submit_data():
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

    asyncio.create_task(evalute_helper(
        problem, dataset, test_data, submission_id))

    return {'msg': 'Success'}


async def evalute_helper(problem: str, dataset: str, test_data: str, submission_id: str):
    submission.add_score(submission_id, dataset)

    loaded_problem = get_problem(problem)

    error, result = loaded_problem.evaluate(dataset, test_data)

    submission.update_score(submission_id, dataset, error,
                            result if error else None,
                            result if not error else None)
