import bottle
from soa.tracks.core import Track


class DSA(Track):
    slug = "dsa"
    title = "Data structures and algorithms"
    description = "Data structures and how they are used in algorithms."

    @property
    def is_locked(self):
        python = Track.trackmap["python"]
        return (
            hasattr(bottle.request, "user")
            and not bottle.request.user.is_.anon
            and not bottle.request.user.has_completed_track(python)
        )


Track.tracks.append(DSA())
