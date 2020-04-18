import os
import json
import markdown
from pathlib import Path
from bs4 import BeautifulSoup
from collections import namedtuple
from textwrap import dedent


class Track:
    tracks = []
    slug = None
    title = None
    description = None
    is_locked = True


def load_tracks():
    """
    Tracks and tasks are kept in RAM so that we don't need to hit the DB
    everytime someone requests a task. Only when they make a submission we
    hit the DB.
    """
    global Track
    Task = namedtuple("Task", "slug order html trackslug checking_fns")
    tracks = []
    for track in Track.tracks:
        tasks = []
        trackpath = Path("soa") / "tracks" / track.slug
        for task in os.listdir(trackpath):
            checking_fns = {}
            if task.endswith("md"):
                with open(trackpath / task, "r") as fl:
                    html = markdown.markdown(fl.read())
                soup = BeautifulSoup(html, "lxml")
                for code in list(soup.findAll("code", attrs={"class": "code_checker"})):
                    pycode = "\n".join(
                        [
                            line
                            for line in code.decode_contents().split("\n")
                            if line.strip() != ""
                        ]
                    )
                    pycode = dedent(pycode)
                    l = {}
                    exec(pycode, globals(), l)
                    for k, v in l.items():
                        checking_fns[k] = v
                    code.decompose()
                html = str(
                    soup
                )  # No need to tell the participants how the code is checked
            else:
                continue
            order = int(task.split(".")[0])
            tasks.append(
                Task(f"{track.slug}{order}", order, html, track.slug, checking_fns)
            )
        tasks = tuple(sorted(tasks, key=lambda x: x.order))
        track.tasks = tasks
        tracks.append(track)
    Track.tracks = tracks
    Track.trackmap = {t.slug: t for t in Track.tracks}
    Track.taskmap = {task.slug: task for track in Track.tracks for task in track.tasks}
