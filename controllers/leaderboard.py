from flask import Blueprint, jsonify

from repositories import problem

leaderboard_controller = Blueprint(
    'leaderboard', __name__, url_prefix='/leaderboard')


@leaderboard_controller.route('/<id>', methods=['GET'])
def get_leaderboard(id: str):
    """get leaderboard of the problem by id."""
    return jsonify(problem.get_problem_leaderboard(id)), 200
