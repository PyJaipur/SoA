from soa.tracks.core import Track
from soa import settings


def answer1(s):
    return "=" == s.replace(" ", "").strip()


def answer2(s):
    return s.strip() == "somesome"


def answer3(s):
    return s.strip() == "zero"


def answer4(s):
    return s.strip().lower() == "true"


class Python(Track):
    slug = "python"
    title = "Python"
    description = (
        "The basics of python that you'll need to complete the rest of the tracks."
    )
    is_locked = False if settings.is_dev else True
    tasks_meta = {
        "py.1": {"order": 1, "md": "1.md", "check": {"answer": answer1}},
        "py.2": {"order": 2, "md": "2.md", "check": {"answer": answer2}},
        "py.3": {"order": 3, "md": "3.md", "check": {"answer": answer3}},
        "py.4": {"order": 4, "md": "4.md", "check": {"answer": answer4}},
    }
