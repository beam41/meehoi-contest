from flask import Flask
from controller import submit_controller

app = Flask(__name__)
app.register_blueprint(submit_controller)
