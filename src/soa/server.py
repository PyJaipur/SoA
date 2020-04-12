import bottle
from soa.settings import redis_host
from bottle_tools import fill_args
from soa.models import Session
import redis

redis = redis.Redis(host=redis_host, port=6379, db=0)


def render(template_name, **kwargs):
    kwargs.update({"current_user": bottle.request.user, "request": bottle.request})
    return bottle.jinja2_template(template_name, **kwargs)


app = bottle.Bottle()


@app.get("/")
def home():
    return render("base.html")
