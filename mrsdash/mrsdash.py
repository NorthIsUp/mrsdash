from gevent import monkey
monkey.patch_all()

from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect

from time_helpers import display_time
from time_helpers import get_times

app = Flask(__name__)

app.config.from_object(__name__)
app.config.from_object('default_settings')
app.config.from_object('local_settings')


@app.route('/favicon.ico')
def favicon():
    return redirect('/static/favicon.ico')


@app.route("/")
def charts():
    #DASHES is an orderd dict

    dashes = app.config['DASHES'](app, request)

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
