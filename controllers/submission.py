import asyncio
from flask import Blueprint, jsonify
from flask_jwt_extended.utils import get_jwt_identity
from flask_jwt_extended.view_decorators import jwt_required

from repositories import submission

submission_controller = Blueprint(
    'submission', __name__, url_prefix='/submission')


@submission_controller.route('/problem/<problem_id>', methods=['GET'])
@jwt_required()
def get_submission_in_problem(problem_id: str):
    """
    Get all submission in problem by problem_id.
    """
    user_id = get_jwt_identity()
    return jsonify(submissions=[submission.to_submission_dto() for submission in submission.get_submissions_in_problem(problem_id, user_id)])


@submission_controller.route('/<id>', methods=['GET'])
@jwt_required()
def get_submission(id: str):
    """
    Get submission by id.

    :param id: Id of the submission
    """
    user_id = get_jwt_identity()
    return jsonify(submission.get_submission(id, user_id).to_submission_with_score_dto())


@submission_controller.route('/<submission_id>/score/<dataset_id>', methods=['GET'])
@jwt_required()
async def get_score(submission_id: str, dataset_id: str):
    """
    get score of the submission. and continue retry if the score is not ready.

    :param id: Id of the submission
    """
    user_id = get_jwt_identity()

    if not submission.check_submission_owner(submission_id, user_id):
        return {'msg': 'You are not the owner of this submission'}, 403

    score = submission.get_score(submission_id, dataset_id)
    tries = 0
    while score.is_running == True and tries < 10:
        await asyncio.sleep(1)
        score = submission.get_score(submission_id, dataset_id)
        tries += 1

    if tries == 10:
        return {'msg': 'Score is not ready'}, 408

    return jsonify(score.to_score_dto())
