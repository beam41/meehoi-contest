from models import Problem, Dataset, Score, Submission, User, Leaderboard
from database import db
from sqlalchemy.sql.expression import func, true
from sqlalchemy.orm.util import aliased
from sqlalchemy import insert
from models.dto import LeaderboardDto


def aggregate_problem_leaderboard():
    """
    aggregate best score of the problem;

    My god why is this so complicated!!

    :param id: id of the problem
    :param user_id: id of the user
    """
    # TODO: should order by score and if score is same, order by submission date

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
        .filter(Score.dataset_id.in_(dataset)) \
        .filter(Score.submission_id.in_(submission)) \
        .group_by(Score.dataset_id) \
        .subquery()

    sum_score = db.session \
        .query(func.sum(best_score.c[0])) \
        .select_from(best_score) \
        .scalar_subquery()

    # this chain for getting best time
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
        .filter(Submission.problem_id == Problem.id) \
        .filter(Score.score == best_score_by_dst) \
        .group_by(Score.dataset_id) \
        .correlate(User, Problem) \
        .subquery()

    best_time = db.session \
        .query(func.max(best_time_list.c[0])) \
        .select_from(best_time_list) \
        .scalar_subquery()

    query = db.session \
        .query(
            User.id,
            Problem.id,
            sum_score,
            best_time,
            func.rank().over(
                order_by=sum_score,
                partition_by=Problem.id
            ),
            func.row_number().over(
                order_by=[sum_score, best_time],
                partition_by=Problem.id
            )
        ) \
        .join(Problem, true())

    ins = insert(Leaderboard).from_select([
        Leaderboard.user_id,
        Leaderboard.problem_id,
        Leaderboard.score,
        Leaderboard.best_time,
        Leaderboard.rank,
        Leaderboard.row_number,
    ], query)

    Leaderboard.query.delete()
    result = db.session.execute(ins)
    db.session.commit()


def get_problem_leaderboard(id) -> LeaderboardDto:
    pass
