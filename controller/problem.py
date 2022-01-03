from operator import itemgetter
from flask import request, Blueprint, jsonify
from model import Problem

problem_controller = Blueprint('problem', __name__, url_prefix='/problem')


@problem_controller.route('/all', methods=['GET'])
def get_problems():
    return jsonify(Problem.query.order_by(Problem.index).all())
