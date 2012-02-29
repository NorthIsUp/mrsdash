from __future__ import absolute_import
from flask.blueprints import Blueprint
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
from flask import current_app

from mrsdash.lib.time_helpers import display_time
from mrsdash.lib.time_helpers import get_times

from mrsdash.lib.helpers import make_module

blueprint = Blueprint(__name__, 'mrsdash')


@blueprint.route('/favicon.ico')
def favicon():
    return redirect('/static/favicon.ico')


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

    return render_template('index.html', **d)


__views_attrs = {
    'favicon': favicon,
    'charts': charts,
    }

views = make_module("views", **__views_attrs)

print views
