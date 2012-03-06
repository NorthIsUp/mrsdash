from __future__ import absolute_import
from flask import current_app
from flask import render_template
from flask import request
from flask import url_for
from flask.blueprints import Blueprint
# from mrsdash.lib.helpers import make_module
from mrsdash.lib.time_helpers import display_time
from mrsdash.lib.time_helpers import get_times
from path import path

from logging import getLogger
logger = getLogger(__name__)

here = path(__file__).dirname().abspath()
template_folder = path(here / "templates")
static_folder = path(here / "static")

print template_folder

blueprint = Blueprint(
    'mrsdash',
    __name__,
    template_folder=template_folder,
    static_url_path="/s",
    static_folder=static_folder,
    )


@blueprint.route('/favicon.ico')
def favicon():
    return url_for('static', filename='favicon.ico')


@blueprint.route("/")
def charts():
    dashes = current_app.config['DASHES'](current_app, request)

    time = request.args.get('time', '1h')
    hide_deploys = request.args.get('hide_deploys', False)

    d = {
        'time': time,
        'current_url': url_for('.charts'),
        'times': get_times(),
        'dashboards': dashes,
        'hide_deploys': hide_deploys,
        'the_time': display_time(time)
        }

    return render_template('dashboard/index.html', **d)


# __views_attrs = {
#     'favicon': favicon,
#     'charts': charts,
#     'blueprint': blueprint,
#     '__add_to_sys_modules': True,
#     }

# views = make_module(__name__ + ".views", **__views_attrs)
