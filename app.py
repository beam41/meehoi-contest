import traceback

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from werkzeug.exceptions import HTTPException

from controllers import *
from database import db
from models.dto import ErrorDto

migrate = Migrate()


def create_app():
    app = Flask(__name__, static_folder='static')
    app.config.from_object('config')

    CORS(app)
    setup_database(app)
    register_blueprints(app)
    JWTManager(app)

    @app.errorhandler(Exception)
    def handle_exception(e: Exception):
        """base exception handle if not handled by controller"""
        if isinstance(e, HTTPException):
            return ErrorDto(str(e), e.code).to_request()

        traceback.print_exc()
        return ErrorDto(str(e), 500).to_request()

    return app


def setup_database(app: Flask):
    with app.app_context():
        db.init_app(app)
        db.create_all()
        migrate.init_app(app, db)


def register_blueprints(app: Flask):
    app.register_blueprint(submit_controller)
    app.register_blueprint(problem_controller)
    app.register_blueprint(user_controller)
    app.register_blueprint(submission_controller)
    app.register_blueprint(leaderboard_controller)
