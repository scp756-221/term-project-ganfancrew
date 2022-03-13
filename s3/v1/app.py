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

def load_db():
    global db
    with open(DB_PATH, 'r') as inp:
        rdr = csv.reader(inp)
        next(rdr)  # Skip header line
        for artist, songtitle, id in rdr:
            db[id] = (artist, songtitle)


@bp.route('/health')
def health():
    return ""


@bp.route('/readiness')
def readiness():
    return ""


@bp.route('/', methods=['GET'])
def list_all():
    global database
    response = {
        "Count": len(database),
        "Items":
            [{'Artist': value[0], 'SongTitle': value[1], 'music_id': id}
             for id, value in database.items()]
    }
    return response

@bp.route('/sort', methods=['GET'])
def list_all_sort():
    global database
    response = {
        "Count": len(database),
        "Items":
            [{'Artist': value[0], 'SongTitle': value[1], 'music_id': id}
             for id, value in database.items()]
    }
    lists = response["Items"]
    lists.sort(key = lambda x:x['SongTitle'], reverse=True)
    r = {
        "Count": len(database),
        "Items": lists
    }
    print(r)
    return r

@bp.route('/artist/<artist>', methods=['GET'])
def list_artist(artist):
    #print(artist)
    global database
    response = {
        "Count": len(database),
        "Items":
            [{'Artist': value[0], 'SongTitle': value[1], 'music_id': id}
             for id, value in database.items()]
    }
    lists = response["Items"]
    items = []
    for i in lists:
        if i['Artist'] == artist.strip():
            tmpItem = {}
            tmpItem["music_id"] = i['music_id']
            tmpItem["Artist"] = i['Artist']
            tmpItem["SongTitle"] = i['SongTitle']
            items.append(tmpItem)
            #print("{}  {:20.20s} {}".format(i['music_id'],i['Artist'],i['SongTitle']))

    #print(items)
    r = {
        "Count": len(items),
        "Items": items
    }
    print(r)
    return r

@bp.route('/deleteAll', methods=['GET'])
def delete_song_all():
    global database
    response = {
        "Count": len(database),
        "Items":
            [{'Artist': value[0], 'SongTitle': value[1], 'music_id': id}
             for id, value in database.items()]
    }
    lists = response["Items"]
    for i in lists:
        print(i['music_id'])
        delete_song(i['music_id'])


    return ''

@bp.route('/<music_id>', methods=['GET'])
def get_song(music_id):
    global database
    if music_id in database:
        value = database[music_id]
        response = {
            "Count": 1,
            "Items":
                [{'Artist': value[0],
                  'SongTitle': value[1],
                  'music_id': music_id}]
        }
    else:
        response = {
            "Count": 0,
            "Items": []
        }
        return app.make_response((response, 404))
    return response


@bp.route('/', methods=['POST'])
def create_song():
    global database
    try:
        content = request.get_json()
        Artist = content['Artist']
        SongTitle = content['SongTitle']
    except Exception:
        return app.make_response(
            ({"Message": "Error reading arguments"}, 400)
            )
    music_id = str(uuid.uuid4())
    database[music_id] = (Artist, SongTitle)
    response = {
        "music_id": music_id
    }
    return response


@bp.route('/<music_id>', methods=['DELETE'])
def delete_song(music_id):
    global database
    if music_id in database:
        del database[music_id]
    else:
        response = {
            "Count": 0,
            "Items": []
        }
        return app.make_response((response, 404))
    return {}


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

    load_db()
    app.logger.error("Unique code: {}".format(ucode))
    p = int(sys.argv[1])
    app.run(host='0.0.0.0', port=p, threaded=True)
