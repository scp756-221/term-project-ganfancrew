"""
SFU CMPT 756
Sample application---music service.
"""

# Standard library modules
import logging
import os
import sys

# Installed packages
from flask import Blueprint
from flask import Flask
from flask import request
from flask import Response

from prometheus_flask_exporter import PrometheusMetrics

import requests

import simplejson as json

# Local modules
import unique_code

# The unique exercise code
# The EXER environment variable has a value specific to this exercise
ucode = unique_code.exercise_hash(os.getenv('EXER'))

# The application

app = Flask(__name__)

metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Music process')

db = {
    "name": "http://cmpt756db:30002/api/v1/datastore",
    "endpoint": [
        "read",
        "write",
        "delete"
    ]
}
bp = Blueprint('app', __name__)


@bp.route('/health')
@metrics.do_not_track()
def health():
    return Response("", status=200, mimetype="application/json")


@bp.route('/readiness')
@metrics.do_not_track()
def readiness():
    return Response("", status=200, mimetype="application/json")


@bp.route('/', methods=['GET'])
def list_all():
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')
    # list all songs here
    return {}


@bp.route('/', methods=['POST'])
def create_playlist():
    headers = request.headers

    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')  
    try:
        content = request.get_json()
        Playlist = content['Playlist']
    except Exception:
        return json.dumps({"message": "error reading arguments"})
    url = db['name'] + '/' + db['endpoint'][1]
    response = requests.post(
        url,
        json={"objtype": "playlist", "Playlist": Playlist},
        headers={'Authorization': headers['Authorization']})
    return (response.json())
        

@bp.route('/test', methods=['GET'])
def test():
    # This value is for user scp756-221
    if ('a7a2998d24e65de2f79f5696e3ab088dea3821111756d9fb6e58c8eaaff74644' !=
            ucode):
        raise Exception("Test failed")
    return {}


@bp.route('/shutdown', methods=['GET'])
def shutdown():
    # From https://stackoverflow.com/questions/15562446/how-to-stop-flask-application-without-using-ctrl-c # noqa: E501
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return {}


app.register_blueprint(bp, url_prefix='/api/v1/playlist/')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        logging.error("missing port arg 1")
        sys.exit(-1)

    # app.logger.error("Unique code: {}".format(ucode))
    p = int(sys.argv[1])
    app.run(host='0.0.0.0', port=p, threaded=True)
