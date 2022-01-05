import traceback
from flask import Flask
from werkzeug.exceptions import HTTPException
from os import path
from flask_jwt_extended import JWTManager

from database import db
from controllers import leaderboard_controller, submit_controller, problem_controller, user_controller, submission_controller


def create_app():
    app = Flask(__name__, static_folder='static')
    app.config.from_object('config')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
        path.join(app.root_path, 'app.db')

    setup_database(app)
    register_blueprints(app)
    JWTManager(app)

    @app.errorhandler(Exception)
    def handle_exception(e: Exception):
        """base exception handle if not handled by controller"""
        if isinstance(e, HTTPException):
            return {"error": True, "message": str(e)}, e.code

        traceback.print_exc()
        return {"error": True, "message": "Internal Server Error"}, 500

    return app


def setup_database(app: Flask):
    with app.app_context():
        db.init_app(app)
        db.create_all()


def register_blueprints(app: Flask):
    app.register_blueprint(submit_controller)
    app.register_blueprint(problem_controller)
    app.register_blueprint(user_controller)
    app.register_blueprint(submission_controller)
    app.register_blueprint(leaderboard_controller)
