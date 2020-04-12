import bottle
from soa.settings import redis_host
from bottle_tools import fill_args
from soa import models
import redis

redis = redis.Redis(host=redis_host, port=6379, db=0)


def render(template_name, **kwargs):
    current_user = models.AnonUser()
    if hasattr(bottle.request, "user"):
        current_user = bottle.request.user
    kwargs.update({"current_user": current_user, "request": bottle.request})
    return bottle.jinja2_template(template_name, **kwargs)


app = bottle.Bottle()


@app.get("/")
def home():
    return render("base.html")


@app.get("/login")
def login():
    return render("login.html")


@app.post("/login")
@fill_args
def login(email):
    return render("login.html")


@app.get("/dashboard")
def login():
    return render("dashboard.html")
