import bottle
from soa.tracks.core import Track


class ADSA(Track):
    slug = "adsa"
    title = "Advanced DSA"
    description = "Advanced data structures and how they are used in algorithms."

    @property
    def is_locked(self):
        dsa = Track.trackmap["dsa"]
        return (
            hasattr(bottle.request, "user")
            and not bottle.request.user.is_.anon
            and not bottle.request.user.has_completed(dsa)
        )


Track.tracks.append(ADSA())
