from disqus.flask import create_app
from path import path
import logging


logger = logging.getLogger(__name__)


blueprints = [
    {'name': 'dashboard', 'url_prefix': '/iapi/dashboard'},
]


def pre_config(app):
    pass


def post_config(app):
    pass


def load_middlewares(app):
    return app

bp_path = path(__file__).dirname().abspath().joinpath('blueprints')
_application = create_app("mrsdash", blueprints, bp_path, pre_config, post_config)
_application = load_middlewares(_application)

application = _application

print application.url_map
