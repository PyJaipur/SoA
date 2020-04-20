from gevent import monkey

monkey.patch_all()
from soa import settings
from soa import models
from soa import server

app = server.app
