import traceback
from flask import Flask
from controller import submit_controller
from werkzeug.exceptions import HTTPException

app = Flask(__name__, static_folder='static')
app.register_blueprint(submit_controller)


# base exception handle if not handled by controller
@app.errorhandler(Exception)
def handle_exception(e: Exception):
    if isinstance(e, HTTPException):
        return {"error": True, "message": str(e)}, e.code

    traceback.print_exc()
    return {"error": True, "message": "Internal Server Error"}, 500
