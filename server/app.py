#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    # all_bakeries = Bakery.query().all()   # =>TypeError: 'Query' object is not callable
    all_bakeries = db.session.query(Bakery).all()

    bakeries = []
    # turn data into python dict obj
    for bakery in all_bakeries:
        bakery_dict = {
            'id': bakery.id,
            "name": bakery.name,
            "created_at": bakery.created_at,
            "updated_at": bakery.updated_at
        }
        bakeries.append(bakery_dict)

    response = make_response(
        # convert data to json format
        # wraps it in a response obj with application/json mimetype
        jsonify(bakeries),
        200,
    )
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = db.session.query(Bakery).filter(Bakery.id==id).first()
    # bakery = db.session.query(Bakery).filter_by(id=id).first()
    bakery_dict = bakery.to_dict()
    response = make_response(bakery_dict, 200)
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = db.session.query(BakedGood).order_by(BakedGood.price)
    
    goods_list = []
    for good in baked_goods:
        good_dict = {
            'id': good.id,
            "name": good.name,
            "price": good.price,
            "created_at": good.created_at,
            "updated_at": good.updated_at,
            "bakery_id": good.bakery_id
        }
        goods_list.append(good_dict)
    response = make_response(jsonify(goods_list), 200)
    response.headers["Content-Type"] = 'application/json'
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = db.session.query(BakedGood).order_by(BakedGood.price.desc())[0]
    good_dict = most_expensive.to_dict()
    response = make_response(good_dict, 200)
    response.headers["Content-Type"] = "application/json"
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
