import yaml
from sys import stderr, argv
from pprint import pprint
from daniel import new_route
from flask import Flask, jsonify, request, abort, make_response

app = Flask(__name__)
db = {}


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
            return res
        except _ as e:
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
        'date_deli': pack['date_sent'],  # todo: real predicted delivery date
        'route': pack['route'],
        'lines': pack['lines'],
        'product': {
            'name': 'product.name',  # todo: real product name
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
        app.jinja_env.auto_reload = True
        app.config['TEMPLATES_AUTO_RELOAD'] = True
        app.run(debug=True, host=host, port=int(port))
    except _ as e:
        print(e)
        # save_db(db, db_path)
        exit(1)
