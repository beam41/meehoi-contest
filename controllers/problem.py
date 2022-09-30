import traceback
from operator import itemgetter
from os import listdir, path

from flask import request, Blueprint, jsonify, current_app
from flask_jwt_extended.utils import get_jwt_identity
from flask_jwt_extended.view_decorators import jwt_required

from models.dto import ErrorDto
from problems import get_problem as get_problem_obj
from repositories import problem, dataset as dataset_repo

problem_controller = Blueprint('problem', __name__, url_prefix='/problem')


@problem_controller.route('/all', methods=['GET'])
@jwt_required()
def get_problems():
    return jsonify(problems=[problem.to_problem_with_index() for problem in problem.get_all_problem()])


@problem_controller.route('/generate', methods=['POST'])
def generate_problem():
    """
    (Admin only)
    Before generate problem we need to recheck something

    - Create problem folder in `static` folder with name match `problem_id`
    - Place your dataset in your problem folder, it has to end with `.in` like `a_test.in`
    (start with alphabet is optional but the function match index of dataset name in body field with index of file sorted alphabetically)
    - Place your problem description in the folder with name `problem_[problem_id].pdf`
    - Create new problem class to evaluate your problem in `problems` folder with `id` match `problem_id` and import in `__init__.py`

    body:
        id: id of the problem
        name: Name of the problem
        dataset: list of the name of the dataset, will be match by index with file sorted alphabetically
    """
    if request.headers.get('x-admin-key') != current_app.config['ADMIN_SPECIAL_KEY']:
        return ErrorDto("You are not authorized to perform this action.", 403).to_request()
    try:
        problem_id, name, dataset = itemgetter(
            'id', 'name', 'dataset')(request.json)

        # check if problems class exist
        if get_problem_obj(problem_id) is None:
            return ErrorDto("Problems class exist not exist").to_request()

        folder_name = path.join(current_app.static_folder, problem_id)
        if not path.exists(folder_name):
            return ErrorDto("Folder not exist").to_request()

        dataset_files = [f for f in listdir(folder_name) if path.isfile(
            path.join(folder_name, f)) and f.endswith('.in')]

        dataset_files.sort()

        if len(dataset_files) != len(dataset):
            return ErrorDto("Number of dataset is not match").to_request()

        problem.add_problem(problem_id, name)
        dataset_repo.add_dataset_m(problem_id, [(dataset_files[i].split('.')[
                                                     0], dataset[i]) for i in range(len(dataset))])

        return {"complete": True}, 200
    except Exception as e:
        traceback.print_exc()
        return ErrorDto(str(e), 500).to_request()


@problem_controller.route('/<id>', methods=['GET'])
def get_problem(id: str):
    """Get individual problem with dataset"""
    return jsonify(problem.get_problem(id).to_problem_with_dataset())


@problem_controller.route('/<id>/best', methods=['GET'])
@jwt_required()
def get_problem_best(id: str):
    """
    Get best score of the problem by id.
    """
    user_id = get_jwt_identity()

    return jsonify(problem.get_problem_bestscore(id, user_id))
