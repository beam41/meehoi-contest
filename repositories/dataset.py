from database import db
from models import Dataset


def get_all_dataset(problem_name: str) -> list[Dataset]:
    """
    get a dataset of a problem

    :param problem_name: name of the problem
    """
    problem = db.session.query(Dataset.id).filter_by(name=problem_name).scalar_subquery()
    return Dataset.query.filter(Dataset.id.in_(problem)).all()


def add_dataset(problem_id: str, name: str) -> str:
    """
    add a new dataset to a problem

    :param problem_id: id of the problem
    :param name: name of the dataset

    :return: id of the new dataset
    """
    dataset = Dataset(name=name, problem_id=problem_id)
    db.session.add(dataset)
    db.session.commit()
    db.session.refresh(dataset)
    return dataset.id


def add_dataset_m(problem_id: str, id_w_name: list[(str, str)]):
    """
    add a new dataset to a problem (multiple)

    this function do not return dataset id

    :param problem_id: id of the problem
    :param id_w_name: id mapped with name of the dataset
    """
    datasets = [Dataset(id=id, name=name, problem_id=problem_id)
                for (id, name) in id_w_name]
    db.session.bulk_save_objects(datasets)
    db.session.commit()
