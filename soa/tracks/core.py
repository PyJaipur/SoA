import os
import json
import markdown
from pathlib import Path
from collections import namedtuple


class Track:
    tracks = []
    slug = None
    title = None
    description = None
    locked = True


def load_tracks():
    """
    Tracks and tasks are kept in RAM so that we don't need to hit the DB
    everytime someone requests a task. Only when they make a submission we
    hit the DB.
    """
    global Track
    Task = namedtuple("Task", "slug order html trackslug")
    tracks = []
    for track in Track.tracks:
        tasks = []
        trackpath = Path("soa") / "tracks" / track.slug
        for task in os.listdir(trackpath):
            if task.endswith("md"):
                with open(trackpath / task, "r") as fl:
                    html = markdown.markdown(fl.read())
            elif task.endswith("html"):
                with open(trackpath / task, "r") as fl:
                    html = fl.read()
            else:
                continue
            order = int(task.split(".")[0])
            tasks.append(Task(f"{track.slug}{order}", order, html, track.slug))
        tasks = tuple(sorted(tasks, key=lambda x: x.order))
        track.tasks = tasks
        tracks.append(track)
    Track.tracks = tracks
    Track.trackmap = {t.slug: t for t in Track.tracks}
    Track.taskmap = {task.slug: task for track in Track.tracks for task in track.tasks}
