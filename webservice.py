# coding: utf8
from flask import Flask, json, request, Response, abort, redirect
from optparse import OptionParser
from drink import Drink
from order import Order
from utils import jsonify

app = Flask(__name__)

drinks = { \
    'Drink1' : Drink('Drink 1', Vodka= 0, Cola=140, Rum=10, IceCube=1),
    'Drink2' : Drink('Drink 2', Vodka=10, Cola=140, Rum= 0, IceCube=0),
    'Drink3' : Drink('Drink 3', Vodka=30, Cola=120, Rum= 0, IceCube=1),
}

orders = dict()
order_id = 0

@app.route('/')
def welcome():
    return jsonify('Welcome to the Smart Cocktail Factory')

@app.route('/drinks')
def get_drinks():
    return jsonify(drinks.keys())

@app.route('/drinks/<drink_id>/recipe')
def get_drink_recipe(drink_id):
    global order_id
    if not drink_id in drinks.keys():
        abort(404)
    return jsonify(drinks[drink_id].recipe) #TODO units?

@app.route('/orders/<drink_id>', methods=['PUT'])
def order_drink(drink_id):
    global order_id
    if not drink_id in drinks.keys():
        abort(404)
    order_id += 1
    orders[order_id] = Order(order_id, drink_id, drinks[drink_id].recipe, 'pending')
    return jsonify(order_id)

@app.route('/admin/orders')
def get_orders():
    serialized_orders = [o.serializeToJson() for o in orders.values()]
    return jsonify(serialized_orders)

@app.route('/admin/orders/clear', methods=['PUT'])
def clear_orders():
    global orders, order_id
    orders = dict()
    order_id = 0
    return jsonify('OK')

@app.route('/factory/orders/pending')
def get_pending_orders():
    serialized_orders = [o.serializeToJson() for o in orders.values() if o.status == 'pending']
    return jsonify(serialized_orders)

@app.route('/factory/orders/next', methods=['PUT'])
def get_next_order():
    pending_order_ids = [o_id for o_id in orders if orders[o_id].status == 'pending']
    if len(pending_order_ids) == 0:
        return jsonify(dict())
    allocated_order_id = min(pending_order_ids)
    orders[allocated_order_id].status = 'in progress'
    response = { 'order_id' : allocated_order_id, 'recipe' : orders[allocated_order_id].recipe }
    return jsonify(response)

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-b", "--bind-address", default='localhost', dest="bind_address", help="bind to ip-address/host BIND_ADDRESS")
    (options, args) = parser.parse_args()
    app.run(host=options.bind_address, port=12345, debug=True)
