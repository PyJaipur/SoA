import bottle
import requests
from bottle_tools import fill_args
from soa import models, plugins, mailer, settings
import redis

redis = redis.Redis(host=settings.redis_host, port=6379, db=0)


def render(template_name, **kwargs):
    kwargs.update({"request": bottle.request})
    return bottle.jinja2_template(template_name, **kwargs)


app = bottle.Bottle()
for plugin in [plugins.AutoSession, plugins.CurrentUser, plugins.LoginRequired]:
    app.install(plugin())


## -------------- routes


@app.get("/", name="landing")
def home():
    if bottle.request.user.is_anon:
        return bottle.redirect("get_login")
    return bottle.redirect("dashboard")


@app.get("/login", skip=["login_required"], name="get_login")
def login():
    return render("login.html")


@app.post("/login", skip=["login_required"])
@fill_args
def login_post(email: str, LoginToken, User):
    u = models.get_or_create(
        bottle.request.session,
        User,
        defaults={"email": email, "username": "?", "permissions": []},
        email=email,
    )
    token = LoginToken.loop_create(bottle.request.session, user=u)
    mailer.send_otp(email, token.otp)
    return bottle.redirect(app.get_url("get_login", otp_sent=True))


@app.get("/otp", skip=["login_required"], name="otp")
@fill_args
def otp(q: str, LoginToken):
    tok = (
        bottle.request.session.query(LoginToken)
        .filter_by(otp=q, is_consumed=False)
        .first()
    )
    if tok is None:
        bottle.abort(404, "No such otp found.")
    tok.is_consumed = True
    bottle.request.session.commit()
    bottle.response.set_cookie(
        settings.cookie_name,
        tok.token,
        secret=settings.secret,
        max_age=3600 * 24 * 60,
        **settings.cookie_kwargs
    )
    return bottle.redirect("/dashboard")


@app.get("/logout", name="logout")
def logout():
    bottle.request.token.has_logged_out = True
    bottle.request.session.commit()
    bottle.response.delete_cookie(key=settings.cookie_name, **settings.cookie_kwargs)
    return bottle.redirect("/")


@app.get("/dashboard", name="dashboard")
def dashboard():
    return render("dashboard.html")
