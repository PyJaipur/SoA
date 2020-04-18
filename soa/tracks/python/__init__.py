from soa.tracks.core import Track


t = Track()
t.slug = "python"
t.title = "Python"
t.description = (
    "The basics of python that you'll need to complete the rest of the tracks."
)
Track.tracks.append(t)
