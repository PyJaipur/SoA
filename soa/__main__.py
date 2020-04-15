import argparse
import logging
from soa import app, settings

if settings.is_dev:
    log = logging.getLogger("soa")
    log.setLevel(logging.DEBUG)
    log.addHandler(logging.StreamHandler())

parser = argparse.ArgumentParser()
parser.add_argument("--port", default=8000, type=int)
args = parser.parse_args()

app.run(port=args.port, host="0.0.0.0", reloader=True, debug=True)
