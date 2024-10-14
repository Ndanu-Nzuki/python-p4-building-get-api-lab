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

# GET /bakeries: returns a list of JSON objects for all bakeries
@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()
    bakeries_list = [bakery.to_dict() for bakery in bakeries]
    return make_response(jsonify(bakeries_list), 200)

# GET /bakeries/<int:id>: returns a single bakery as JSON with its baked goods nested in a list
@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = db.session.get(Bakery, id)  # Updated to use db.session.get()
    if bakery is None:
        return make_response(jsonify({"error": "Bakery not found"}), 404)
    
    # Create a dictionary to include all relevant fields, including created_at and updated_at
    bakery_dict = {
        "id": bakery.id,
        "name": bakery.name,
        "created_at": bakery.created_at,  # Include created_at
        "updated_at": bakery.updated_at,  # Include updated_at
        "baked_goods": [{"id": good.id, "name": good.name, "price": good.price} for good in bakery.baked_goods]
    }
    return make_response(jsonify(bakery_dict), 200)

# GET /baked_goods/by_price: returns a list of baked goods sorted by price in descending order
@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_list = [baked_good.to_dict() for baked_good in baked_goods]
    return make_response(jsonify(baked_goods_list), 200)

# GET /baked_goods/most_expensive: returns the single most expensive baked good
@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    return make_response(jsonify(most_expensive.to_dict()), 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
