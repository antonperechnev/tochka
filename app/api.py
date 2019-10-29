from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask import request, jsonify, Response
from flasgger import Swagger
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
import uuid
import json
import atexit

from DB.table_flask import db, Clients
# from DB.tables import Clients

from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


cache = Cache(config={'CACHE_TYPE': 'simple'})
app = Flask(__name__)
cache.init_app(app)
Swagger(app)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['SQLALCHEMY_POOL_RECYCLE'] = 3600
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Anton1995@localhost/tochka'

db.init_app(app)


def hold_update():
    '''
    engine = create_engine('postgresql://postgres:Anton1995@localhost/tochka', isolation_level="AUTOCOMMIT")
    meta = MetaData(engine)
    base = declarative_base()
    Session = sessionmaker(engine)
    session = Session()
    users = session.query(Clients).all()
    '''
    users = Clients.query.all()
    for user in users:
        if user.balance - user.hold > 0:
            user.balance -= user.hold
            user.hold = 0
    db.session.commit()


sched = BackgroundScheduler(daemon=True)
sched.add_job(hold_update, 'interval', minutes=5)
sched.start()


class User:
    def __init__(self, data):
        self.user_id = uuid.UUID(data['id'])
        try:
            self.amount = int(data['amount'])
        except KeyError:
            pass
        self.user_db = Clients.query.filter_by(uuid=self.user_id).first()
        self.response_status = 200
        # self.result = True

    def addition_create(self, fio='', balance='', user_status=''):
        return {'status': user_status,
                'balance': balance,
                'fio': fio,
                'id': self.user_id}

    def user_handler(self, result: bool, description: dict, balance=0):
        try:
            user_status = self.user_db.status
            user_balance = balance or self.user_db.balance
            user_fio = self.user_db.fio

            addition = self.addition_create(user_fio, user_balance, user_status)
        except AttributeError:
            addition = self.addition_create()  # maybe = {}
            result = False
            description['explanation'] = 'user not exist'

        return {'addition': addition, 'result': result, 'description': description}


@app.route('/api/ping')
def ping():
    """
                Tochka test API

                ---
                tags:
                  - ping method
                responses:
                  400:
                    description: Bad request
                  200:
                    description: OK
                  500:
                    description: INTERNAL SERVER ERROR



    """
    return jsonify(status='OK')


@app.route('/api/add', methods=['POST'])
def add():
    """
                Tochka test API

                ---
                tags:
                  - add method
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



    """
    try:
        data: dict = request.get_json(force=True)
    except Exception as e:
        return Response(f'{e}', status=400)

    result = True
    description = {}
    user = User(data)
    db_connect = user.user_db
    if db_connect.status == 'закрыт':
        description = {'explanation': "Can't do operation. Bank account is closed"}
        user_balance = db_connect.balance - db_connect.hold
        result = False
    elif db_connect.balance - db_connect.hold < 0:

        user_balance = db_connect.balance
        db_connect.hold -= user.amount
        description = {'explanation': f"Hold is more than balance. Now you debt is {db_connect.hold}"}
        if user.amount > db_connect.hold:
            db_connect.balance -= db_connect.hold
            db_connect.hold = 0
            user_balance = db_connect.balance
        db.session.commit()
    else:
        user_balance = db_connect.balance + user.amount - db_connect.hold
        db_connect.balance += user.amount
        db.session.commit()

    resp = user.user_handler(result=result, description=description, balance=user_balance)

    addition, result, description = resp['addition'], resp['result'], resp['description']
    return jsonify(addition=addition,
                   status=user.response_status, result=result, description=description)


@app.route('/api/substract', methods=['POST'])
def substract():
    """
                Tochka test API

                ---
                tags:
                  - substract method
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



    """
    try:
        data: dict = request.get_json(force=True)
    except Exception as e:
        return Response(f'{e}', status=400)
    result = True
    description = {}
    user = User(data)
    db_connect = user.user_db
    if db_connect.balance - db_connect.hold - user.amount >= 0 and db_connect.status == 'открыт':
        # update hold in db
        db_connect.hold += user.amount
        user_balance = db_connect.balance - db_connect.hold
        db.session.commit()
    else:
        user_balance = db_connect.balance
        result = False
        description = {'explanation': "Can't do operation. Not enough money"}
        if db_connect.status == 'закрыт':
            description = {'explanation': "Can't do operation. Bank account is closed"}

    resp = user.user_handler(result=result, description=description, balance=user_balance)

    addition, result, description = resp['addition'], resp['result'], resp['description']
    return jsonify(addition=addition,
                   status=user.response_status, result=result, description=description)


@app.route('/api/status', methods=['POST'])
def status():
    """
                Tochka test API

                ---
                tags:
                  - status method
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



    """
    try:
        data: dict = request.get_json(force=True)
    except Exception as e:
        return Response(f'{e}', status=400)

    result = True
    description = {}

    user = User(data)
    db_connect = user.user_db
    user_balance = db_connect.balance - db_connect.hold
    resp = user.user_handler(result=result, description=description, balance=user_balance)

    addition, result, description = resp['addition'], resp['result'], resp['description']
    return jsonify(addition=addition,
                   status=user.response_status, result=result, description=description)


if __name__ == '__main__':
    app.run(debug=True)


# {"id": "26c940a1-7228-4ea2-a3bc-e6460b172040", "amount": 500}