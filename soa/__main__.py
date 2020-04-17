import argparse
import logging
from soa import app, settings, models

if settings.is_dev:
    log = logging.getLogger("soa")
    log.setLevel(logging.DEBUG)
    log.addHandler(logging.StreamHandler())

parser = argparse.ArgumentParser()
parser.add_argument("--port", default=8000, type=int)
parser.add_argument("--email", default=None, type=str)
parser.add_argument("--add-perm", default=None, type=str)
args = parser.parse_args()

if args.email and args.add_perm:  # Add a new perm to the given user
    session = models.Session()
    u = session.query(models.User).filter_by(email=args.email).first()
    if u is not None:
        u.permissions = list(set(u.permissions + [args.add_perm]))
        session.commit()
    session.close()
else:
    app.run(port=args.port, host="0.0.0.0", reloader=True, debug=True)
