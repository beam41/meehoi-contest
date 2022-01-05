from sqlalchemy.orm import aliased
from sqlalchemy.dialects import sqlite
from models import Problem, Dataset, Score, Submission, User
from database import db
from sqlalchemy.sql.expression import func, text

from models.dto import BestScoreDto, best_score_dto, leaderboard_dto, LeaderboardDto


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


def get_problem_bestscore(id: str, user_id: str) -> BestScoreDto:
    """
    get best score of the problem by id.

    :param id: id of the problem
    :param user_id: id of the user
    """
    dataset = db.session.query(Dataset.id).filter_by(
        problem_id=id).scalar_subquery()
    submission = db.session.query(Submission.id).filter_by(
        user_id=user_id).scalar_subquery()

    return best_score_dto.from_query_result(
        db.session.query(Score.dataset_id, func.max(Score.score))
        .group_by(Score.dataset_id)
        .having(Score.dataset_id.in_(dataset))
        .having(Score.submission_id.in_(submission))
        .all()
    )


def get_problem_leaderboard(id: str) -> LeaderboardDto:
    """
    get best score of the problem by id.

    :param id: id of the problem
    :param user_id: id of the user
    """

    dataset = db.session \
        .query(Dataset.id) \
        .filter_by(problem_id='zoo') \
        .scalar_subquery()

    submission = db.session \
        .query(Submission.id) \
        .filter(text("user_id = users.id")) \
        .scalar_subquery()

    max_score = db.session.query(func.max(Score.score).label('score')) \
        .group_by(Score.dataset_id) \
        .having(Score.dataset_id.in_(dataset)) \
        .having(Score.submission_id.in_(submission)) \
        .subquery('max_score')

    sum_score = db.session \
        .query(func.sum(max_score.columns.get('score'))) \
        .select_from(max_score) \
        .scalar_subquery()

    return leaderboard_dto.from_query_result(db.session.query(User.id, User.username, sum_score).all())
