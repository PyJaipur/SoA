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
    tasks_meta = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        trackmap[getattr(cls, "slug")] = cls


def load_tracks():
    """
    Tracks and tasks are kept in RAM so that we don't need to hit the DB
    everytime someone requests a task. Only when they make a submission we
    hit the DB.
    """
    Task = namedtuple("Task", "title slug order md html trackslug checking_fns score")
    for track in trackmap.values():
        tasks = []
        trackpath = Path("soa") / "tracks" / track.slug
        title = None
        for slug, task in (
            track.tasks_meta.items() if track.tasks_meta is not None else []
        ):
            print("Loading", trackpath, task)
            with open(trackpath / task["md"], "r") as fl:
                lines = list(fl.readlines())
                for line in lines:
                    if line.strip().startswith("#"):
                        title = line.strip().lstrip("#")
                        break
                task["html"] = markdown.markdown("".join(lines))
            tasks.append(
                Task(
                    title,
                    slug,
                    task["order"],
                    task["md"],
                    task["html"],
                    track.slug,
                    task["check"],
                    track.score,
                )
            )
        tasks = tuple(sorted(tasks, key=lambda x: x.order))
        track.tasks = tasks
    trackmap.update({k: v() for k, v in trackmap.items()})
    taskmap.update(
        {task.slug: task for track in trackmap.values() for task in track.tasks}
    )
