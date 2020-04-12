import argparse
from soa import app

parser = argparse.ArgumentParser()
parser.add_argument("--port", default=8000, type=int)
args = parser.parse_args()

app.run(port=args.port, reloader=True, debug=True)
