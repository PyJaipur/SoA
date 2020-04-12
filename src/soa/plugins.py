from soa import models


class Plugin:
    name = None
    api = 2

    def apply(self, callback, route):
        raise NotImplemented

    def setup(self, app):
        pass


class CurrentUser(Plugin):
    name = "current_user"

    def apply(self, callback, route):
        # Check cookies
        bottle.request.user = modes.AnonUser()
        return callback
