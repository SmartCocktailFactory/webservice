# coding: utf8
from flask import Flask, json, request, Response, abort, redirect
from drink import Drink
from order import Order
from utils import jsonify

app = Flask(__name__)

drinks = { \
  #                              [Vodka ml]   [Cola ml]    [Rum ml]    [Ice cubes]
    'Drink1' : Drink('Drink 1', [  0,           140,          10,            1 ]),
    'Drink2' : Drink('Drink 2', [  10,          140,           0,            0 ]),
    'Drink3' : Drink('Drink 3', [  30,          120,           0,            1 ]),
}

orders = dict()
order_id = 0

@app.route('/')
def welcome():
    return jsonify('Welcome to the Smart Cocktail Factory')

@app.route('/drinks')
def get_drinks():
    return jsonify(drinks.keys())

@app.route('/orders/<drink_id>', methods=['PUT'])
def order_drink(drink_id):
    global order_id
    if not drink_id in drinks.keys():
        abort(404)
    order_id += 1
    orders[order_id] = Order(order_id, drink_id, drinks[drink_id].recipe, 'pending')
    return jsonify(order_id)

@app.route('/orders')
def get_orders():
    return jsonify([(o.order_id, o.drink_id, o.recipe, o.status) for o in orders.values()])

@app.route('/factory/orders/clear', methods=['PUT'])
def clear_orders():
    global orders
    orders = dict()
    return jsonify('OK')

@app.route('/factory/orders/pending')
def get_pending_orders():
    pending_orders = [o for o in orders.values() if o.status == 'pending']
    serialized_orders = [o.serializeToJson() for o in pending_orders]
    return jsonify(serialized_orders)

@app.route('/factory/orders/next', methods=['PUT'])
def get_next_order():
    pending_orders = [o for o in orders.values() if o.status == 'pending']
    if len(pending_orders) == 0:
        return jsonify(dict())
    allocated_order_id = min(orders)
    allocated_order = orders[allocated_order_id]
    allocated_order.status = 'in progress'
    return allocated_order.serializeToJson()

if __name__ == '__main__':
    app.run(host='localhost', port=12345, debug=True)
