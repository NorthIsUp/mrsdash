import os
from path import path

LOCAL_SETTINGS_ENVVAR = 'MRSDASH_SETTINGS'
os.environ[LOCAL_SETTINGS_ENVVAR] = path(__file__).dirname().abspath() / 'local_settings.py'


LISTEN_HOST = '0.0.0.0'
CANONICAL_NAME = LISTEN_HOST

# When behind a load balancer, set CANONICAL_PORT to the value contained in
# Host headers (normally it will be '80' in production)
# 8000 chosen to mesh with gunicorn
CANONICAL_PORT = '9000'

DEBUG = True

# If users want to pass specific werkzeug options
WERKZEUG_OPTS = {
    'host': LISTEN_HOST,
    'port': int(CANONICAL_PORT)
    }

# Global configuration
BROWSER_SECRET_KEY = ''

# When behind a load balancer, set CANONICAL_NAME to the value contained in
# Host headers (e.g. 'www.example.org')
CANONICAL_NAME = 'localhost'
LISTEN_HOST = '0.0.0.0'

# When behind a load balancer, set CANONICAL_PORT to the value contained in
# Host headers (normally it will be '80' in production)
# 8000 chosen to mesh with gunicorn
CANONICAL_PORT = '8000'

DEBUG_TOOLBAR = False
PASSWORD_HASH = ''
SECRET_KEY = ''
USE_SSL = False

COOKIE_NAME = 'b'
COOKIE_PATH = '/'

LOGGING_CONFIG = "config/logging.json"
LOGGING_DICTCONFIG = ""  # auto generated from path above

GRAPHITE_BASE_URL = ''
GRAPHITE_DEPLOYS = []


def DASHES(app, request):
    """This should return an OrderedDict of the following format:
    {'heading': [Graph(), ...], ...}"""
    from mrsdash.lib.graphite import Graph
    from collections import OrderedDict
    dashes = OrderedDict()

    config = {
        'GRAPHITE_BASE_URL': GRAPHITE_BASE_URL,
        'GRAPHITE_DEPLOYS': GRAPHITE_DEPLOYS
        }

    dashes['My Stats'] = []
    dashes['My Stats'].append(Graph(config, '1h'))

    return dashes
