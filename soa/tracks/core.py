import os
import json
import markdown
from pathlib import Path
from bs4 import BeautifulSoup
from collections import namedtuple
from textwrap import dedent


trackmap = {}
taskmap = {}


class Track:
    slug = None
    title = None
    description = None
    is_locked = True
    score = 1

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        trackmap[getattr(cls, "slug")] = cls


def load_tracks():
    """
    Tracks and tasks are kept in RAM so that we don't need to hit the DB
    everytime someone requests a task. Only when they make a submission we
    hit the DB.
    """
    Task = namedtuple("Task", "slug order html trackslug checking_fns score")
    for track in trackmap.values():
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
                Task(
                    f"{track.slug}{order}",
                    order,
                    html,
                    track.slug,
                    checking_fns,
                    track.score,
                )
            )
        tasks = tuple(sorted(tasks, key=lambda x: x.order))
        track.tasks = tasks
    trackmap.update({k: v() for k, v in trackmap.items()})
    taskmap.update(
        {task.slug: task for track in trackmap.values() for task in track.tasks}
    )
