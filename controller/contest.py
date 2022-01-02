from operator import itemgetter
from flask import request, Blueprint, jsonify
from model.contest import Contest

contest_controller = Blueprint('contest', __name__)

@contest_controller.route('/contests', methods=['GET'])
def get_contests():
    return jsonify(Contest.query.order_by(Contest.index).all())
