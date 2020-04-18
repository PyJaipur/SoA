import bottle
import redis
from collections import namedtuple
from datetime import datetime
from soa import models, settings
from functools import wraps

R = redis.from_url(settings.redis_url)
DAY_STRF = "%Y.%m.%d"
Alert = namedtuple("Alert", "title message")


def per_day_limit(name, n):
    def wrapper2(fn):
        @wraps(fn)
        def wrapper(*a, **kw):
            ts = datetime.utcnow().strftime(DAY_STRF)
            keyname = name + ":" + ts
            current = R.get(keyname)
            current = int(current.decode()) if current is not None else 0
            if current is not None and current > n:
                raise bottle.abort(429, "Please retry later")
            else:
                with R.pipeline() as pipe:
                    pipe.incr(keyname)
                    pipe.expire(keyname, 24 * 60 * 60)
                    pipe.execute()
                return fn(*a, **kw)

        return wrapper

    return wrapper2


def render(template_name, **kwargs):
    kwargs.update(
        {"request": bottle.request, "alerts": getattr(bottle.request, "alerts", [])}
    )
    return bottle.jinja2_template(template_name, **kwargs)


def alert(msg, *, title=None):
    "Flash an error message to the user"
    if not hasattr(bottle.request, "alerts"):
        bottle.request.alerts = []
    bottle.request.alerts.append(Alert(title, msg))


class Plugin:
    name = None
    api = 2

    def apply(self, callback, route):
        raise NotImplemented

    def setup(self, app):
        self.app = app


class AutoSession(Plugin):
    name = "auto_session"

    def apply(self, callback, route):
        @wraps(callback)
        def wrapper(*a, **kw):
            bottle.request.session = models.Session()
            try:
                return callback(*a, **kw)
            finally:
                bottle.request.session.close()

        return wrapper


class CurrentUser(Plugin):
    name = "current_user"

    def apply(self, callback, route):
        @wraps(callback)
        def wrapper(*a, **kw):
            # Check cookies
            user = models.AnonUser()
            cook = bottle.request.get_cookie(
                settings.cookie_name, secret=settings.secret
            )
            if cook is not None:
                token = (
                    bottle.request.session.query(models.LoginToken)
                    .filter_by(token=cook, has_logged_out=False)
                    .first()
                )
                bottle.request.token = token
                if token is not None:
                    user = token.user
            bottle.request.user = user
            return callback(*a, **kw)

        return wrapper


class LoginRequired(Plugin):
    name = "login_required"

    def apply(self, callback, route):
        @wraps(callback)
        def wrapper(*a, **kw):
            if bottle.request.user.is_.anon:
                return bottle.redirect(
                    self.app.get_url("get_login", next_url=bottle.request.url)
                )
            return callback(*a, **kw)

        return wrapper


class LastLogin(Plugin):
    name = "last_login"

    def encourage_user(self, score):
        "Encourage the person everyday"
        if score == 1:
            alert(
                "🎉 +1 point."
                "Every day you login you get a point since the secret to doing anything well is to do it everyday.",
                title="Daily login",
            )
        elif score < 5:
            alert("🎉 +1 point", title="Daily login")
        elif score < 10:
            alert(
                "🎉 +1 point. You're really good at this! Good job!", title="Daily login"
            )

    def apply(self, callback, route):
        @wraps(callback)
        def wrapper(*a, **kw):
            if bottle.request.user.is_.anon:
                return callback(*a, **kw)
            ll = bottle.request.user.last_seen
            if ll is None:
                bottle.request.user.login_score = 1
                self.encourage_user(bottle.request.user.login_score)
                bottle.request.session.commit()
            elif ll.date() < datetime.utcnow().date():
                bottle.request.user.login_score = bottle.request.user.login_score + 1
                self.encourage_user(bottle.request.user.login_score)
                bottle.request.session.commit()
            try:
                return callback(*a, **kw)
            finally:
                bottle.request.user.last_seen = datetime.utcnow()
                bottle.request.session.commit()

        return wrapper
