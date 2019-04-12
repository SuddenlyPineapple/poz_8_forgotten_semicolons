import yaml
from sys import stderr, argv
from pprint import pprint
from flask import Flask, jsonify, request, abort, make_response

app = Flask(__name__)
DB = 'magic/mock.yml'
db = {}


def log(*args):
    print(file=stderr, *args)


def load_db():
    global db
    with open(DB, 'r') as file:
        try:
            db = yaml.load(file)
        except yaml.YAMLError as e:
            print('database exception', e)


def save_db():
    global db
    with open(DB, 'w') as file:
        yaml.dump(db, file)


def massage_poi(dict):
    x, y = dict['cord']
    return {'x': x, 'y': y, 'name': dict['addr'], 'date': dict['date']}


@app.route('/paczki', methods=['GET'])
def paczki():
    id = request.args.get('user')
    if id not in db['users']:
        return make_response(jsonify({"error": f"user {id} not in database"}), 400)
    user = db['users'][id]
    res = {
        'user_id': id,
        'paczki': user['pack'],
    }
    return jsonify(res)


@app.route('/paczka_stan', methods=['GET'])
def paczka_stan():
    id = request.args.get('id')
    if id not in db['packs']:
        return make_response(jsonify({'error': f'package {id} not in database'}), 400)
    res = {
        'pack_id': id,
        'curr_coord': [0, 0],
        'curr_route': 0,
        'curr_state': 'curr_state',
    }
    return jsonify(res)


@app.route('/paczka_info', methods=['GET'])
def paczka_info():
    id = request.args.get('id')
    if id not in db['packs']:
        return make_response(jsonify({'error': f'package {id} not in database'}), 400)
    pack = db['packs'][id]
    user_id = pack['user_id']
    date_sent = pack['date_sent']
    route = [massage_poi(poi) for poi in pack['route']]
    res = {
        'pack_id': id,
        'user_id': user_id,
        'date_sent': date_sent,
        'date_deli': date_sent,  # todo: real predicted delivery date
        'route': route,
        'lines': [],  # todo: lines to draw on map
        'product': {
            'name': 'product.name',  # todo: real product name
        },
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
    if len(argv) < 3:
        log(f'usage: {program} 0.0.0.0 6060')
        exit(1)

    _, host, port = argv
    try:
        load_db()
        app.jinja_env.auto_reload = True
        app.config['TEMPLATES_AUTO_RELOAD'] = True
        app.run(debug=True, host=host, port=int(port))
    except:
        save_db()
