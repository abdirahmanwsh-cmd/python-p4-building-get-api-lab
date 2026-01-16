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
    # Query all bakeries from the database and serialize them to JSON
    # The serialize() method converts the model objects to dictionaries based on serialize_rules
    bakery_list = [bakery.to_dict() for bakery in Bakery.query.all()]
    return make_response(jsonify(bakery_list), 200)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    # Find a single bakery by its ID and serialize it to JSON
    # The to_dict() includes nested baked_goods due to the relationship
    bakery = Bakery.query.filter(Bakery.id == id).first()
    if bakery:
        return make_response(jsonify(bakery.to_dict()), 200)
    else:
        return make_response(jsonify({'error': 'Bakery not found'}), 404)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    # Query all baked goods and sort them by price in descending order
    # desc() method sorts in descending order (highest prices first)
    baked_goods_list = [bg.to_dict() for bg in BakedGood.query.order_by(BakedGood.price.desc()).all()]
    return make_response(jsonify(baked_goods_list), 200)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    # Query baked goods sorted by price in descending order, then limit to 1 result
    # first() gets only the first result (the most expensive one)
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if most_expensive:
        return make_response(jsonify(most_expensive.to_dict()), 200)
    else:
        return make_response(jsonify({'error': 'No baked goods found'}), 404)

if __name__ == '__main__':
    app.run(port=5555, debug=True)