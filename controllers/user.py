from operator import itemgetter
from flask import request, Blueprint
from os import makedirs, path
from flask_jwt_extended import create_access_token
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


@user_controller.route("/login", methods=["POST"])
def login():
    username, password = itemgetter(
        'username', 'password')(request.json)
    user_ = user.get_user(username, password)
    if user_ is None:
        return {"error": True, "message": "Wrong Username or Password"}, 401

    access_token = create_access_token(identity=user_.id)
    return {'access_token': access_token, 'username': user_.username, 'id': user_.id}
