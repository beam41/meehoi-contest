from operator import itemgetter
from flask import request, Blueprint, jsonify, current_app
from os import listdir, path

from problems import get_problem
from repositories import problem, dataset as dataset_repo

problem_controller = Blueprint('problem', __name__, url_prefix='/problem')


@problem_controller.route('/all', methods=['GET'])
def get_problems():
    # TODO: return dto
    return jsonify(list(map(lambda x: x.to_all_problem_dto(), problem.get_all_problem())))


@problem_controller.route('/generate', methods=['POST'])
def generate_problem():
    """
    Before generate problem we need to recheck something

    - Create problem folder in `static` folder with name match `problem_id`
    - Place your dataset in your problem folder, it has to end with `.in` like `a_test.in`
    (start with alphabet is optional but the function match index of dataset name in body field with index of file sorted alphabetically)
    - Create new problem class to evaluate your problem in `problems` folder with `id` match `problem_id` and import in `__init__.py`

    body:
        id: id of the problem
        name: Name of the problem
        dataset: list of the name of the dataset, will be match by index with file sorted alphabetically
    """
    problem_id, name, dataset = itemgetter(
        'id', 'name', 'dataset')(request.json)

    # check if problems class exist
    if get_problem(problem_id) is None:
        return {
            "error": True,
            "message": "Problems class exist not exist"
        }, 400

    folder_name = path.join(current_app.static_folder, problem_id)
    if not path.exists(folder_name):
        return {
            "error": True,
            "message": "Folder not exist"
        }, 400

    dataset_files = [f for f in listdir(folder_name) if path.isfile(
        path.join(folder_name, f)) and f.endswith('.in')]

    dataset_files.sort()

    if len(dataset_files) != len(dataset):
        return {
            "error": True,
            "message": "Number of dataset is not match"
        }, 400

    problem.add_problem(problem_id, name)
    dataset_repo.add_dataset_m(problem_id, [(dataset_files[i].split('.')[
                               0], dataset[i]) for i in range(len(dataset))])

    return {"complete": True}, 200
