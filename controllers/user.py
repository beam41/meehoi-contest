from operator import itemgetter
from flask import request, Blueprint, current_app as app
from os import makedirs, path
import nanoid
import traceback

from problems import get_problem
from repositories import user
from utils.alpha import safe_alpha


user_controller = Blueprint('user', __name__, url_prefix='/user')


@user_controller.route('/', methods=['POST'])
def add_user():
    """
    (Admin only)
    Add user and autogenerate password.

    body:
        username: username of the user
    """
    try:
        username = request.json['username']
        pwd = nanoid.generate(alphabet=safe_alpha, size=6)
        user.add_user(username, pwd)
        return {"message": "User added (pwd: {})".format(pwd)}
    except Exception as e:
        traceback.print_exc()
        return {
            "error": True,
            "message": str(e)
        }, 500
