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


GRAPHITE_BASE_URL = ''
GRAPHITE_DEPLOYS = []
