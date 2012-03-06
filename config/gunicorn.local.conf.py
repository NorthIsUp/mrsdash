from gevent import monkey
monkey.patch_all()

from mrsdash import default_settings as ds
import logging
import os
import signal
import sys

bind = "{0}:{1}".format(ds.CANONICAL_NAME, ds.CANONICAL_PORT)
worker_class = 'gevent'
# Message duplication problems right now, don't increase beyond 1
workers = 1
worker_connections = 10000


def on_starting(server):
    # use server hook to patch socket to allow worker reloading
    from gevent import monkey
    monkey.patch_socket()


def when_ready(server):
    def monitor():
        modify_times = {}
        while True:
            for module in sys.modules.values():
                path = getattr(module, "__file__", None)
                if not path:
                    continue
                if path.endswith(".pyc") or path.endswith(".pyo"):
                    path = path[:-1]
                try:
                    modified = os.stat(path).st_mtime
                except:
                    continue
                if path not in modify_times:
                    modify_times[path] = modified
                    continue
                if modify_times[path] != modified:
                    logging.info("%s modified; restarting server", path)
                    os.kill(os.getpid(), signal.SIGHUP)
                    modify_times = {}
                    break
            gevent.sleep(1)

    import gevent
    gevent.spawn(monitor)
