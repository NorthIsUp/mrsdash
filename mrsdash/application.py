from disqus.flask import create_app
from greplin.scales.flaskhandler import registerStatsHandler
from path import path
import logging


logger = logging.getLogger(__name__)


blueprints = [
    {'name': 'mrsdash', 'url_prefix': '/'},
]


def pre_config(app):
    pass


def post_config(app):
    logger.info("starting post_config")

    # make this a normal blueprint registration (fix in scales library)
    registerStatsHandler(app, __name__, prefix="/iapi/status")
    logger.info("done with post_config")


def load_middlewares(app):
    return app

bp_path = path(__file__).dirname().abspath().joinpath('blueprints')
_application = create_app("mrsdash", blueprints, bp_path, pre_config, post_config)
_application = load_middlewares(_application)

application = _application
