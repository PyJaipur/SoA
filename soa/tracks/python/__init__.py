from soa.tracks.core import Track
from soa import settings


class Python(Track):
    slug = "python"
    title = "Python"
    description = (
        "The basics of python that you'll need to complete the rest of the tracks."
    )
    is_locked = False if settings.is_dev else True
    gh_issue_map = {1: 19}
