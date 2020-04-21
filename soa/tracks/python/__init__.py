from soa.tracks.core import Track


class Python(Track):
    slug = "python"
    title = "Python"
    description = (
        "The basics of python that you'll need to complete the rest of the tracks."
    )
    is_locked = True
    gh_issue_map = {1: 19}
