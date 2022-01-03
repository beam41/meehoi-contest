from models import User
from database import db


def add_user(username: str, password: str) -> str:
    """
    Create a new user

    :param username: username of the user
    :param password: password of the user
    :return: id of the user
    """
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    db.session.refresh(user)
    return user.id
