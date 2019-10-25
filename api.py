from flask import Flask
from flask import request, jsonify, Response
from flasgger import Swagger
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
import uuid
import json

from DB.table_flask import db, Clients
# from DB.tables import Clients

cache = Cache(config={'CACHE_TYPE': 'simple'})
app = Flask(__name__)
cache.init_app(app)
Swagger(app)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['SQLALCHEMY_POOL_RECYCLE'] = 3600
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Anton1995@localhost/tochka'

db.init_app(app)


def addition_create(uuid='', fio='', balance='', user_status=''):
    return {'status': user_status,
            'balance': balance,
            'fio': fio,
            'id': uuid}


def user_info_handler(user_info, user_id, amount=0, add=False, substract=False):
    description = {}
    result =True
    try:
        user_status = user_info.status
        user_balance = user_info.balance
        if add:
            user_info.balance += amount
            user_balance = user_info.balance
            db.session.commit()
        user_fio = user_info.fio
        addition = addition_create(user_id, user_fio, user_balance, user_status)
    except AttributeError:
        addition = addition_create()  # maybe = {}
        result = False
        description = {'explanation': 'user not exist'}

    return {'addition': addition, 'result': result, 'description': description}


@app.route('/api/ping')
def ping():
    """
                Tochka test API

                ---
                tags:
                  - Return ping
                responses:
                  400:
                    description: Bad request
                  200:
                    description: OK
                  500:
                    description: INTERNAL SERVER ERROR
                  401:
                    description: Unauthorized


    """
    return jsonify(status='OK')


@app.route('/api/add', methods=['POST'])
def add():
    """
                Tochka test API

                ---
                tags:
                  - add amount
                parameters:
                  - name: info
                    in: body
                    type: json
                    description: dict description in wrike
                responses:
                  400:
                    description: Bad request
                  200:
                    description: OK
                  500:
                    description: INTERNAL SERVER ERROR
                  401:
                    description: Unauthorized


    """
    try:
        data: dict = request.get_json(force=True)
    except Exception as e:
        return Response(f'{e}', status=400)

    user_id = uuid.UUID(data['id'])
    amount = int(data['amount'])
    user_info = Clients.query.filter_by(uuid=user_id).first()
    response_status = 200
    resp = user_info_handler(user_info, user_id, amount=amount, add=True)
    # db.session.commit()
    addition, result, description = resp['addition'], resp['result'], resp['description']
    return jsonify(addition=addition,
                   status=response_status, result=result, description=description)


@app.route('/api/substract', methods=['POST'])
def substract():
    """
                Tochka test API

                ---
                tags:
                  - Return ping
                parameters:
                  - name: info
                    in: body
                    type: json
                    description: dict description in wrike
                responses:
                  400:
                    description: Bad request
                  200:
                    description: OK
                  500:
                    description: INTERNAL SERVER ERROR
                  401:
                    description: Unauthorized


    """


@app.route('/api/status', methods=['POST'])
def status():
    """
                Tochka test API

                ---
                tags:
                  - Return User status
                parameters:
                  - name: data
                    in: body
                    type: json
                    description: dict
                responses:
                  400:
                    description: Bad request
                  200:
                    description: OK
                  500:
                    description: INTERNAL SERVER ERROR
                  401:
                    description: Unauthorized


    """
    try:
        data: dict = request.get_json(force=True)
    except Exception as e:
        return Response(f'{e}', status=400)

    user_id = uuid.UUID(data['id'])
    user_info = Clients.query.filter_by(uuid=user_id).first()

    result = True if user_info else False
    response_status = 200
    description = {}
    # try/except быстрее, при условии, что чаще идут правильные значения
    try:
        user_status = user_info.status
        user_balance = user_info.balance
        user_fio = user_info.fio
        addition = addition_create(user_id, user_fio, user_balance, user_status)
    except AttributeError:
        addition = addition_create()  # maybe = {}
        result = False
        description = {'explanation': 'user not exist'}
    return jsonify(addition=addition,
                   status=response_status, result=result, description=description)


if __name__ == '__main__':
    app.run(debug=True)