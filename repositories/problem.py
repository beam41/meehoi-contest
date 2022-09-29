from sqlalchemy import union_all
from sqlalchemy.orm import aliased
from sqlalchemy.sql.expression import func, desc

from database import db
from models import Problem, Dataset, Score, Submission, User
from models.dto import BestScoreDto, best_score_dto, ProblemListDto, problem_list_dto, LeaderboardDto, leaderboard_dto


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


def get_problem_leaderboard(id) -> LeaderboardDto:
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
        .filter(Score.is_running.is_(False)) \
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
        .filter(Score.is_running.is_(False)) \
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
        .query(
        User.id,
        User.username,
        sum_score,
        best_time,
        func.rank().over(
            order_by=sum_score.desc(),
        )
    ) \
        .filter(sum_score.isnot(None)) \
        .order_by(desc(sum_score)) \
        .order_by(best_time)

    return leaderboard_dto.from_query_result(query.all())


def get_all_problem_with_rank(user_id: str) -> ProblemListDto:
    """get list of all problems with rank"""
    dataset = db.session \
        .query(Dataset.id) \
        .filter_by(problem_id=Problem.id) \
        .correlate(Problem) \
        .scalar_subquery()

    submission = db.session \
        .query(Submission.id) \
        .filter(Submission.user_id == User.id) \
        .correlate(User) \
        .scalar_subquery()

    best_score = db.session.query(func.max(Score.score)) \
        .filter(Score.is_running.is_(False)) \
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
        .filter(Score.is_running.is_(False)) \
        .filter(score_alias.submission_id.in_(submission)) \
        .filter(score_alias.dataset_id == Score.dataset_id) \
        .group_by(score_alias.dataset_id) \
        .correlate(Score) \
        .scalar_subquery()

    best_time_list = db.session \
        .query(func.min(Submission.created_date)) \
        .join(Score, Score.submission_id == Submission.id) \
        .filter(Submission.user_id == User.id) \
        .filter(Submission.problem_id == Problem.id) \
        .filter(Score.score == best_score_by_dst) \
        .group_by(Score.dataset_id) \
        .correlate(User) \
        .subquery()

    best_time = db.session \
        .query(func.max(best_time_list.c[0])) \
        .select_from(best_time_list) \
        .scalar_subquery()

    rank_query = db.session \
        .query(
        Problem.id,
        func.rank().over(
            order_by=sum_score.desc(),
            partition_by=Problem.id
        ),
        User.id,
        None,
        None,
    ) \
        .filter(sum_score.isnot(None)) \
        .order_by(desc(sum_score)) \
        .order_by(best_time) \
        .subquery()

    query_wrank = db.session.query(rank_query).filter(rank_query.c[2] == user_id)

    query_all_problem = db.session \
        .query(
        Problem.id,
        None,
        None,
        Problem.p_index,
        Problem.name
    )

    query_union = union_all(query_wrank, query_all_problem).subquery()

    query = db.session.query(
        query_union.c[0],
        func.max(query_union.c[1]),
        func.group_concat(query_union.c[3]),
        func.max(query_union.c[4]),
    ) \
        .group_by(query_union.c[0]) \
        .order_by(query_union.c[3])

    return problem_list_dto.from_query_result(query.all())
