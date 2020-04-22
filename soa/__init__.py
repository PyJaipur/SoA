from gevent import monkey
import sys

if sys.path[0] != '':
	sys.path.insert(0, '')
monkey.patch_all()
from soa import settings
from soa import models
from soa import server

app = server.app
