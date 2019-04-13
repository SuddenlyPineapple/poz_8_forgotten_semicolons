#!/usr/bin/env python3

import yaml
from sys import stderr, argv
from pprint import pprint
from daniel import new_route
from flask import Flask, jsonify, request, abort, make_response
import time, threading
from flask_cors import CORS
import datetime

app = Flask(__name__)
CORS(app)
db = {}


def update_times():
    for id in db['packs']:
        if db['packs'][id]['finished'] == False:
            db['packs'][id]['elapsed'] += 1
            db['packs'][id]['finished'] = db['packs'][id]['elapsed'] >= db['packs'][id]['seconds']


def timer():
    threading.Timer(1, timer).start()
    update_times()


def log(*args):
    print(file=stderr, *args)


def load_db(path):
    with open(path, 'r') as file:
        try:
            res = yaml.safe_load(file)
            for id in res['packs']:
                pack = res['packs'][id]
                route = [massage_poi(x) for x in pack['route']]
                res['packs'][id]['route'] = route
                (points, seconds), polyline = new_route([(x['x'], x['y']) for x in route])
                res['packs'][id]['elapsed'] = 0
                res['packs'][id]['points'] = points
                res['packs'][id]['seconds'] = seconds
                res['packs'][id]['date_deli'] = res['packs'][id]['date_sent'] + datetime.timedelta(0, seconds)
                res['packs'][id]['lines'] = polyline
                res['packs'][id]['finished'] = False
            return res
        except Exception as e:
            print('database exception', e)
            exit(1)


def save_db(db, path):
    with open(path, 'w') as file:
        yaml.dump(db, file)


def massage_poi(dict):
    x, y = dict['cord']
    return {'x': x, 'y': y, 'name': dict['addr'], 'date': dict['date']}


def get_pack_info(id):
    if id not in db['packs']:
        return make_response(jsonify({'error': f'package {id} not in database'}), 400)
    pack = db['packs'][id]
    res = {
        'pack_id': id,
        'user_id': pack['user_id'],
        'date_sent': pack['date_sent'],
        'date_deli': pack['date_deli'],
        'route': pack['route'],
        'lines': pack['lines'],
        'product': {
            'name': pack['product']['name'],
        },
    }
    return res


@app.route('/', methods=['GET'])
def index():
    index = """
    allepaczka serwer

    /paczka_info?id=p0
    /paczka_stan?id=p0
    /paczki?user=u0
    """
    return make_response('<br>'.join(index.split('\n')), 200)


@app.route('/paczka_stan', methods=['GET'])
def paczka_stan():
    id = request.args.get('id')
    if id not in db['packs']:
        return make_response(jsonify({'error': f'package {id} not in database'}), 400)
    pack = db['packs'][id]
    finished = pack['finished']
    state = 'Dostarczona' if finished else 'W transporcie'
    coord = [0, 0] if finished else pack['points'][pack['elapsed']]
    res = {
        'pack_id': id,
        'curr_coord': coord,
        'curr_route': 0,
        'curr_state': state,
    }
    return jsonify(res)


@app.route('/paczka_info', methods=['GET'])
def paczka_info():
    id = request.args.get('id')
    return jsonify(get_pack_info(id))


@app.route('/paczki', methods=['GET'])
def paczki():
    id = request.args.get('user')
    if id not in db['users']:
        return make_response(jsonify({"error": f"user {id} not in database"}), 400)
    user = db['users'][id]
    packs = user['pack']
    res = {
        'user_id': id,
        'paczki_id': packs,
        'paczki': list(map(get_pack_info, packs)),
    }
    return jsonify(res)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'bad request'}), 400)


@app.errorhandler(404)
def bad_request(error):
    return make_response(jsonify({'error': 'not found'}), 404)


if __name__ == '__main__':
    program = argv[0]
    if len(argv) < 4:
        log(f'usage: {program} magic/mock.yml 0.0.0.0 6060')
        exit(1)

    _, db_path, host, port = argv
    try:
        db = load_db(db_path)
        timer()
        print('passed')
        app.jinja_env.auto_reload = True
        app.config['TEMPLATES_AUTO_RELOAD'] = True
        app.run(debug=True, host=host, port=int(port))
    except Exception as e:
        print(e)
        # save_db(db, db_path)
        exit(1)
