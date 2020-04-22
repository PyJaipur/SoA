import argparse
import logging
import sys
print(sys.path)
from soa import app, settings, models, housekeeping, tracks

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
    tracks.core.load_tracks()
    kwargs = {
        "port": args.port,
        "host": "0.0.0.0",
    }
    if settings.is_dev:
        kwargs.update(dict(debug=True, reloader=False))
    kwargs["server"] = "gevent"
    app.run(**kwargs)
