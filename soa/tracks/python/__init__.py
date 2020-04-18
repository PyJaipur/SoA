from soa.tracks.core import Track


class Python(Track):
    slug = "python"
    title = "Python"
    description = (
        "The basics of python that you'll need to complete the rest of the tracks."
    )

    @property
    def is_locked(self):
        """
        If this track needs to depend on some other track, change this function
        """
        return False


Track.tracks.append(Python())
