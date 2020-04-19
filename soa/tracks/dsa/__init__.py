import bottle
from soa.tracks.core import Track, trackmap


class DSA(Track):
    slug = "dsa"
    title = "Data structures and algorithms"
    description = "Data structures and how they are used in algorithms."
    score = 2

    @property
    def is_locked(self):
        python = trackmap["python"]
        return (
            hasattr(bottle.request, "user")
            and not bottle.request.user.is_.anon
            and not bottle.request.user.has_completed_track(python)
        )
