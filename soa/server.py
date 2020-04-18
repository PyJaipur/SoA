import bottle
from validate_email import validate_email
import requests
from bottle_tools import fill_args
from soa import models, plugins, mailer, settings, tracks

alert = plugins.alert
render = plugins.render


app = bottle.Bottle()
for plugin in [
    plugins.AutoSession,
    plugins.CurrentUser,
    plugins.LoginRequired,
    plugins.LastLogin,
]:
    app.install(plugin())


## -------------- routes


@app.get("/", name="landing")
def f():
    if bottle.request.user.is_.anon:
        return bottle.redirect("get_login")
    return bottle.redirect(app.get_url("tracks"))


@app.get("/login", skip=["login_required"], name="get_login")
@fill_args
def f(otp_sent=False):
    if otp_sent:
        alert(
            "An email has been sent which contains the login link."
            "Please open that link in your browser in order to login.",
            title="OTP sent",
        )
    return render("login.html")


@app.post("/login", skip=["login_required"])
@fill_args
def f(email: str, LoginToken, User):
    if not validate_email(email):
        return bottle.redirect(app.get_url("get_login", invalid_email=True))
    plugins.within_limits("login", n=300)
    plugins.within_limits(email, n=10)  # a user can only login 10 times a day
    u = models.get_or_create(
        bottle.request.session,
        User,
        defaults={
            "email": email,
            "username": "?",
            "permissions": [],
            "taskprogress": {"done": []},
        },
        email=email,
    )
    u.ensure_email_hash(bottle.request.session)
    token = LoginToken.loop_create(bottle.request.session, user=u)
    mailer.send_otp(email, token.otp)
    return bottle.redirect(app.get_url("get_login", otp_sent=True))


@app.get("/otp", skip=["login_required"], name="otp")
@fill_args
def f(q: str, LoginToken):
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
def f():
    bottle.request.session.delete(bottle.request.token)
    bottle.request.session.commit()
    bottle.response.delete_cookie(key=settings.cookie_name, **settings.cookie_kwargs)
    return bottle.redirect("/")


@app.get("/tracks", name="tracks")
def f():
    return render("tracks.html", page_title="Tracks", tracks=tracks.Track.tracks)


@app.get("/task/<slug>", name="task")
def f(slug):
    task = tracks.Track.taskmap.get(slug)
    if task is None:
        raise bottle.abort(404, "Page not found")
    track = tracks.Track.trackmap[task.trackslug]
    if track.is_locked:
        raise bottle.abort(404, "Page not found")
    return render("task.html", page_title=track.title, current_task=task, track=track)


@app.get("/account", name="get_account")
@fill_args
def f(User, updated=False):
    if updated:
        alert("Updated successfully.",)
    admin_kwargs = {}
    if bottle.request.user.is_.admin:
        admin_kwargs = {"user_count": bottle.request.session.query(User).count()}
    return render("account.html", page_title="Account", **admin_kwargs)


@app.post("/account")
@fill_args
def f(User, username=None, show_email_on_cert=None):
    show_email_on_cert = show_email_on_cert == "on"
    bottle.request.user.username = username
    bottle.request.user.show_email_on_cert = show_email_on_cert
    bottle.request.session.commit()
    return bottle.redirect(app.get_url("get_account", updated=True))


@app.get("/cert/<hsh>", skip=["login_required"])
@fill_args
def f(hsh, User):
    user = bottle.request.session.query(User).filter_by(email_hash=hsh).first()
    if user is None:
        raise bottle.abort(404, "No such page.")
    return render("certificate.html", user=user)
