from soa.tracks.core import Track


class DSA(Track):
    slug = "dsa"
    title = "Data structures and Algorithms"
    description = "Basic data structures and how they are used in algorithms."
    is_locked = False


Track.tracks.append(DSA())
