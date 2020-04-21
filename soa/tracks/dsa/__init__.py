import bottle
from soa.tracks.core import Track, trackmap


class DSA(Track):
    slug = "dsa"
    title = "Data structures and algorithms"
    description = "Data structures and how they are used in algorithms."
    score = 2
    is_locked = True
    gh_issue_map = {1: 20}