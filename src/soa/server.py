import bottle
from bottle_tools import fill_args


tempate = bottle.jinja2_template
app = bottle.Bottle()


@app.get("/")
def home():
    return template("base.html")
