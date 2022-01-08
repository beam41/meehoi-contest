from operator import itemgetter
from flask import request, Blueprint, current_app as app
from os import makedirs, path
from flask_jwt_extended import create_access_token
import nanoid
import traceback
from datetime import datetime
from tzlocal import get_localzone

from problems import get_problem
from repositories import user
from utils.alpha import safe_alpha
from models.dto import ErrorDto

user_controller = Blueprint('user', __name__, url_prefix='/user')


@user_controller.route('', methods=['POST'])
def add_user():
    """
    (Admin only)
    Add user and autogenerate password.

    body:
        username: username of the user
    """
    if request.headers.get('x-admin-key') != app.config['ADMIN_SPECIAL_KEY']:
        return ErrorDto("You are not authorized to perform this action.", 403).to_request()
    try:
        username = request.json['username']
        pwd = nanoid.generate(alphabet=safe_alpha, size=6)
        user.add_user(username, pwd)
        return {"msg": "User added (pwd: {})".format(pwd)}
    except Exception as e:
        traceback.print_exc()
        return ErrorDto(str(e), 500).to_request()


@user_controller.route("/login", methods=["POST"])
def login():
    username, password = itemgetter(
        'username', 'password')(request.json)
    user_ = user.get_user(username, password)
    if user_ is None:
        return ErrorDto("Wrong Username or Password", 403).to_request()

    access_token = create_access_token(identity=user_.id)
    return {
        'access_token': access_token,
        'username': user_.username,
        'id': user_.id,
        'expires_in': (datetime.now(tz=get_localzone()) + app.config['JWT_ACCESS_TOKEN_EXPIRES']).isoformat()
    }
