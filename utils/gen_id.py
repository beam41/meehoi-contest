from nanoid import generate
from .alpha import safe_alpha


def generate_user_id():
    """Generate id using safe string and length 5"""

    return generate(alphabet=safe_alpha, size=5)


def generate_submission_id():
    """Generate id using safe string and length 10"""
    return generate(alphabet=safe_alpha, size=10)
