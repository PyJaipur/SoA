import bottle
from soa.settings import redis_host
from bottle_tools import fill_args
from soa.models import Session
import redis

redis = redis.Redis(host=redis_host, port=6379, db=0)
tempate = bottle.jinja2_template
app = bottle.Bottle()


@app.get("/")
def home():
    return template("base.html")
