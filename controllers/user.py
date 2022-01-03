from operator import itemgetter
from flask import request, Blueprint, current_app as app
from os import makedirs, path

import nanoid

from problems import get_problem
from repositories import user
from utils.alpha import safe_alpha


user_controller = Blueprint('user', __name__, url_prefix='/user')


@user_controller.route('/', methods=['POST'])
def add_user():
    """
    Add user and autogenerate password.

    body:
        username: username of the user
    """
    username = request.json['username']
    pwd = nanoid.generate(alphabet=safe_alpha, size=6)
    user.add_user(username,pwd )
    return {"message": "User added (pwd: {})".format(pwd)}
