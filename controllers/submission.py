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
