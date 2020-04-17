import bottle
import requests
from collections import namedtuple
from bottle_tools import fill_args
from soa import models, plugins, mailer, settings


Alert = namedtuple("Alert", "title message")
Crumb = namedtuple("Crumb", "text link")


def alert(msg, *, title=None):
    "Flash an error message to the user"
    if not hasattr(bottle.request, "alerts"):
        bottle.request.alerts = []
    bottle.request.alerts.append(Alert(title, msg))


def render(template_name, **kwargs):
    kwargs.update(
        {"request": bottle.request, "alerts": getattr(bottle.request, "alerts", [])}
    )
    return bottle.jinja2_template(template_name, **kwargs)


app = bottle.Bottle()
for plugin in [
    plugins.AutoSession,
    plugins.CurrentUser,
    plugins.LoginRequired,
    plugins.AutoCrumbs,
]:
    app.install(plugin())


## -------------- routes


@app.get("/", name="landing")
def home():
    if bottle.request.user.is_.anon:
        return bottle.redirect("get_login")
    return bottle.redirect(app.get_url("tracks"))


@app.get("/login", skip=["login_required"], name="get_login")
@fill_args
def login(otp_sent=False):
    if otp_sent:
        alert(
            "An email has been sent which contains the login link."
            "Please open that link in your browser in order to login.",
            title="OTP sent",
        )
    return render("login.html")


@app.post("/login", skip=["login_required"])
@plugins.per_day_limit("login", n=300)
@fill_args
def login_post(email: str, LoginToken, User):
    u = models.get_or_create(
        bottle.request.session,
        User,
        defaults={"email": email, "username": "?", "permissions": []},
        email=email,
    )
    u.ensure_email_hash(bottle.request.session)
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
    return bottle.redirect(app.get_url("get_account"))


@app.get("/logout", name="logout")
def logout():
    bottle.request.session.delete(bottle.request.token)
    bottle.request.session.commit()
    bottle.response.delete_cookie(key=settings.cookie_name, **settings.cookie_kwargs)
    return bottle.redirect("/")


@app.get("/tracks", name="tracks")
def tracks():
    return render("tracks.html", page_title="Tracks")


@app.get("/task/<taskid>", name="task")
def tracks(taskid, Task):
    task = bottle.request.session.query(Task).filter_by(id=taskid).first()
    if task is None:
        raise bottle.abort(404, "Page not found")
    return render("task.html", title=task.name, task=task, crumbs=task.track.tasks)


@app.get("/account", name="get_account")
@fill_args
def profile(User, updated=False):
    if updated:
        alert("Updated successfully.",)
    admin_kwargs = {}
    if bottle.request.user.is_.admin:
        admin_kwargs = {"user_count": bottle.request.session.query(User).count()}
    return render("account.html", page_title="Account", **admin_kwargs)


@app.post("/account")
@fill_args
def profile(User, username=None, show_email_on_cert=None):
    show_email_on_cert = show_email_on_cert == "on"
    bottle.request.user.username = username
    bottle.request.user.show_email_on_cert = show_email_on_cert
    bottle.request.session.commit()
    return bottle.redirect(app.get_url("get_account", updated=True))


@app.get("/cert/<hsh>", skip=["login_required"])
@fill_args
def cert(hsh, User):
    user = bottle.request.session.query(User).filter_by(email_hash=hsh).first()
    if user is None:
        raise bottle.abort(404, "No such page.")
    return render("certificate.html", user=user)
