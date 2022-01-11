from sqlalchemy.sql.expression import desc
from models import Submission, Score
from database import db


def add_submission(problem_id: str, user_id: str, code_path: str) -> Submission:
    """
    :param problem_id: Id of the problem
    :param user_id: Id of the user

    :return: Submission
    """
    submission = Submission(user_id=user_id, problem_id=problem_id, code_path=code_path)
    db.session.add(submission)
    db.session.commit()
    db.session.refresh(submission)
    return submission


def check_submission_owner(submission_id: str, user_id: str) -> bool:
    """
    :param submission_id: Id of the submission
    :param user_id: Id of the user

    :return: True if the user is the owner of the submission
    """
    return db.session.query(
        Submission.query.filter_by(id=submission_id, user_id=user_id).exists()
    ).scalar()


def update_codepath(submission_id: str, code_path: str):
    """
    :param submission_id: Id of the submission
    :param code_path: Path of the code

    :return: None
    """
    submission = Submission.query.filter_by(id=submission_id).first()
    submission.code_path = code_path
    db.session.commit()


def add_score(submission_id: str, dataset_id: str):
    """
    crate a score object for the submission and dataset with default to running
    :param submission_id: Id of the submission
    :param dataset_id: Id of the dataset
    :param is_error: True if the submission is error
    :param error_txt: Error text
    :param score: Score of the submission + dataset

    :return: None
    """
    score_obj = Score(submission_id=submission_id, dataset_id=dataset_id)
    db.session.add(score_obj)
    db.session.commit()


def update_score(submission_id: str, dataset_id: str, is_error: bool, error_txt: str, score: int):
    """
    :param submission_id: Id of the submission
    :param dataset_id: Id of the dataset
    :param is_error: True if the submission is error
    :param error_txt: Error text
    :param score: Score of the submission + dataset

    :return: None
    """
    score_ = Score.query.filter_by(
        submission_id=submission_id, dataset_id=dataset_id).first()
    score_.is_running = False
    score_.is_error = is_error
    score_.error_txt = error_txt
    score_.score = score
    db.session.commit()


def get_submission(submission_id: str, user_id: str) -> Submission:
    """
    :param problem_id: Id of the problem
    :param user_id: Id of the user

    :return: Id of the submission
    """
    return Submission.query.filter_by(id=submission_id, user_id=user_id).first()


def get_submissions_in_problem(problem_id: str, user_id: str) -> list[Submission]:
    """
    :param problem_id: Id of the problem
    :param user_id: Id of the user

    :return: List of submission
    """
    return Submission.query \
        .filter_by(problem_id=problem_id, user_id=user_id) \
        .order_by(desc(Submission.created_date)) \
        .all()
