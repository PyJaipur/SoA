from soa.tracks.core import Track
from soa import settings
from bottle import request


def a1(s):
    return s == "df.mean()"


def a2(s):
    return s == "df['company'].get_dummies()"


def a3(s):
    return s.lower() == "metrics"


def a4(s):
    return s == "200"


def a5(s):
    return s == "3"


def a6(s):
    return s.lower() == "ward"


def a7(s):
    return s.lower() == "False"


def a8(s):
    return s == "5"


class ML(Track):
    slug = "ml"
    title = "Machine Learning"
    description = "Machine learning"

    @property
    def is_locked(self):
        if request.user.is_.track_owner:
            return False
        return False if settings.is_dev else True

    tasks_meta = {
        "ml.1": {"order": 1, "md": "1.md", "check": {"answer": a1}},
        "ml.2": {"order": 2, "md": "2.md", "check": {"answer": a2}},
        "ml.3": {"order": 3, "md": "3.md", "check": {"answer": a3}},
        "ml.4": {"order": 4, "md": "4.md", "check": {"answer": a4}},
        "ml.5": {"order": 5, "md": "5.md", "check": {"answer": a5}},
        "ml.6": {"order": 6, "md": "6.md", "check": {"answer": a6}},
        "ml.7": {"order": 7, "md": "7.md", "check": {"answer": a7}},
        "ml.8": {"order": 8, "md": "8.md", "check": {"answer": a8}},
    }
