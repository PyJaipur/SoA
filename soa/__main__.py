import argparse
import logging
from soa import app, settings, models, housekeeping

if settings.is_dev:
    log = logging.getLogger("soa")
    log.setLevel(logging.DEBUG)
    log.addHandler(logging.StreamHandler())

parser = argparse.ArgumentParser()
parser.add_argument("--port", default=8000, type=int)
parser.add_argument("--tracks-dir", default="tracks", type=str)
parser.add_argument("--housekeeping", default=None, type=str)
args = parser.parse_args()

if args.housekeeping:
    housekeeping.handle(args)
else:
    models.tracks = models.load_tracks(args.tracks_dir)
    models.trackmap = {track.slug: track for track in models.tracks}
    models.taskmap = {
        task.slug: task for track in models.tracks for task in track.tasks
    }
    app.run(port=args.port, host="0.0.0.0", reloader=True, debug=True)
