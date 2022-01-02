
from .base import Contest
from .zoo import ZooContest


contest_list: dict[str, Contest] = {
    contest.id: contest for contest in [ZooContest()]
}


def get_contest(id: str) -> Contest:
    if (id in contest_list):
        return contest_list[id]
