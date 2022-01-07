from flask import Blueprint, jsonify, request, current_app as app

from repositories import leaderboard
from models.dto import ErrorDto

leaderboard_controller = Blueprint(
    'leaderboard', __name__, url_prefix='/leaderboard')


@leaderboard_controller.route('/<id>', methods=['GET'])
def get_leaderboard(id: str):
    """get leaderboard of the problem by id."""
    return jsonify(leaderboard.get_problem_leaderboard(id)), 200


@leaderboard_controller.route('/aggregate', methods=['GET'])
def aggregate_leaderboard():
    """get leaderboard of the problem by id."""
    if request.headers.get('x-admin-key') != app.config['ADMIN_SPECIAL_KEY']:
        return ErrorDto("You are not authorized to perform this action.", 403).to_request()
    leaderboard.aggregate_problem_leaderboard()
    return {}, 200
