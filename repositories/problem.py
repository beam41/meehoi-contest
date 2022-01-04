from models import Problem
from database import db
from sqlalchemy.sql.expression import func


def get_all_problem() -> list[Problem]:
    """get list of all problems"""
    return Problem.query.order_by(Problem.index).all()


def add_problem(id: str, name: str):
    """
    add a new problem

    use `add_dataset` to generate dataset for this problem

    :param id: id of the problem
    :param name: name of the problem
    """
    max_i = db.session.query(func.max(Problem.index)).one()[0]
    if max_i is None:
        max_i = 0
    problem = Problem(id=id, name=name, index=max_i)
    db.session.add(problem)
    db.session.commit()


def get_problem(id: str) -> Problem:
    """get a problems"""
    return Problem.query.filter_by(id=id).one()
