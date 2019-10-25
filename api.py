from flask import Flask
from flask import request, jsonify, Response
from flasgger import Swagger
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
import uuid

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
    data: dict = request.get_json()
    user_id = uuid.UUID(data['id'])
    user_info = [i for i in Clients.query.filter_by(uuid=user_id).all()]
    return jsonify(addition={'status': user_info[0].status,
                             'balance': user_info[0].balance},
                   status=200, result=True, description={})


if __name__ == '__main__':
    app.run()