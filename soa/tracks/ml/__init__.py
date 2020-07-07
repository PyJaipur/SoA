from soa.tracks.core import Track
from soa import settings
from bottle import request


class ML(Track):
    slug = "ml"
    title = "Machine Learning"
    description = "Machine learning"

    @property
    def is_locked(self):
        if request.user.is_.track_owner:
            return True
        return True if settings.is_dev else False
