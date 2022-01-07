from models import Problem, Dataset, Score, Submission, User
from database import db
from sqlalchemy.sql.expression import desc, func
from sqlalchemy.orm.util import aliased

from models.dto import BestScoreDto, best_score_dto, leaderboard_dto, LeaderboardDto


def get_all_problem() -> list[Problem]:
    """get list of all problems"""
    # TODO: return user rank
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
    """get a problem"""
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
        .filter(Score.submission_id.in_(submission))
        .filter(Score.dataset_id.in_(dataset))
        .group_by(Score.dataset_id)
        .all()
    )


def get_problem_leaderboard(id: str) -> LeaderboardDto:
    """
    get best score of the problem by id.

    My god why is this so complicated!!

    :param id: id of the problem
    :param user_id: id of the user
    """
    # TODO: should order by score and if score is same, order by submission date

    dataset = db.session \
        .query(Dataset.id) \
        .filter_by(problem_id=id) \
        .scalar_subquery()

    submission = db.session \
        .query(Submission.id) \
        .filter(Submission.user_id == User.id) \
        .correlate(User) \
        .scalar_subquery()

    best_score = db.session.query(func.max(Score.score)) \
        .filter(Score.dataset_id.in_(dataset)) \
        .filter(Score.submission_id.in_(submission)) \
        .group_by(Score.dataset_id) \
        .subquery()

    sum_score = db.session \
        .query(func.sum(best_score.c[0])) \
        .select_from(best_score) \
        .scalar_subquery()

    # this chain for sorting by time
    score_alias = aliased(Score)

    best_score_by_dst = db.session.query(func.max(score_alias.score)) \
        .filter(score_alias.submission_id.in_(submission)) \
        .filter(score_alias.dataset_id == Score.dataset_id) \
        .group_by(score_alias.dataset_id) \
        .correlate(Score) \
        .scalar_subquery()

    best_time_list = db.session \
        .query(func.min(Submission.created_date)) \
        .join(Score, Score.submission_id == Submission.id) \
        .filter(Submission.user_id == User.id) \
        .filter(Submission.problem_id == id) \
        .filter(Score.score == best_score_by_dst) \
        .group_by(Score.dataset_id) \
        .correlate(User) \
        .subquery()

    best_time = db.session \
        .query(func.max(best_time_list.c[0])) \
        .select_from(best_time_list) \
        .scalar_subquery()

    query = db.session \
        .query(User.id, User.username, sum_score) \
        .filter(sum_score.isnot(None)) \
        .order_by(desc(sum_score)) \
        .order_by(best_time)

    print(query.statement.compile(compile_kwargs={"literal_binds": True}))

    return leaderboard_dto.from_query_result(query.all())
