from gevent import monkey
import sys

if (
    sys.path[0] != ""
):  # Some redhat distributions are not picking up the current directory in path
    sys.path.insert(0, "")
monkey.patch_all()
