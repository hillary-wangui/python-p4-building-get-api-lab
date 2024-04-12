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
    bakeries = []


    for bakery in Bakery.query.all():
        baked_goods = [{
            "name": goods.name, 
            "price": goods.price,
            "created_at":goods.created_at,
            "updated_at":goods.updated_at
            } 
            for goods in bakery.baked_goods
            ]
        bakeries_dict = {
            "id": bakery.id,
            "created_at": bakery.created_at,
            "name": bakery.name,
            "baked_goods": baked_goods,
            "updated_at":bakery.updated_at
        }
        bakeries.append(bakeries_dict)

    response = make_response(
        jsonify(bakeries),
        200
    )
    response.headers['Content-Type'] = "application/json"
    return response


@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()

    if bakery is None:
        # Return a 404 response if the bakery with the given ID is not found
        return make_response(jsonify({"error": "Bakery not found"}), 404)
    baked_goods = [{
            "name": goods.name, 
            "price": goods.price,
            "created_at":goods.created_at,
            "updated_at":goods.updated_at
            } 
            for goods in bakery.baked_goods
            ]
    bakery_dict = {
        "id":bakery.id,
        "name": bakery.name,
        "created_at": bakery.created_at,
        "baked_goods": baked_goods,
        "updated_at": bakery.updated_at
    }

    response = make_response(
        jsonify(bakery_dict),
        200
    )
    response.headers['Content-Type'] = "application/json"

    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()

    baked_goods_list = [{
        "id":goods.id,
        "name": goods.name, 
        "price": goods.price,
        "created_at":goods.created_at,
        "updated_at": goods.updated_at
        }
        for goods in baked_goods]
    
    response = make_response(
        jsonify(baked_goods_list),
        200
    )
    response.headers['Content-Type'] = 'application/json'

    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive_good = BakedGood.query.order_by(BakedGood.price.desc()).first()

    most_expensive_data = {
        "id": most_expensive_good.id,
        "name": most_expensive_good.name,
        "price": most_expensive_good.price,
        "created_at": most_expensive_good.created_at
    }

    response = make_response(
        jsonify(most_expensive_data),
        200
    )
    response.headers['Content-Type'] = 'application/json'
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)