#!/usr/bin/python
# coding: utf8
from flask import Flask, json, request, Response, abort, redirect
from optparse import OptionParser
from datetime import timedelta
from drink import Drink
from order import Order
from utils import jsonify

app = Flask(__name__)

drinks = { \
    'Drink1' : Drink('Drink 1',           Cola=140, Rum=10, IceCube=1),
    'Drink2' : Drink('Drink 2', Vodka=10, Cola=140),
    'Drink3' : Drink('Drink 3', Vodka=30, Cola=120,         IceCube=1),
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
    if not drink_id in drinks.keys():
        abort(404)
    return jsonify(drinks[drink_id].recipe) #TODO units?

@app.route('/orders/<drink_id>', methods=['POST'])
def order_drink(drink_id):
    global order_id
    if not drink_id in drinks.keys():
        abort(404)
    order_id += 1
    orders[order_id] = Order(order_id, drink_id, drinks[drink_id].recipe, 'pending')
    return jsonify(order_id)

@app.route('/admin/orders')
def get_orders():
    if 'status' in request.args:
        selected_orders = [o for o in orders.values() if o.status == request.args['status']]
    else:
        selected_orders = orders.values()
    serialized_orders = [o.ToJsonConvertableObject() for o in selected_orders]
    return jsonify(serialized_orders)

@app.route('/admin/orders/clear', methods=['PUT', 'GET'])
def clear_orders():
    global orders, order_id
    orders = dict()
    order_id = 0
    return jsonify('OK')

def __get_order_ids_with_status(status):
    return [o_id for o_id in orders if orders[o_id].status == status]

def __get_pending_order_ids():
    return __get_order_ids_with_status('pending')

def __get_in_progress_order_ids():
    return __get_order_ids_with_status('in progress')

@app.route('/factory/orders/next', methods=['POST'])
def get_next_order():
    pending_order_ids = __get_pending_order_ids()
    if len(pending_order_ids) == 0:
        return jsonify(dict())
    allocated_order_id = min(pending_order_ids)
    orders[allocated_order_id].status = 'in progress'
    response = { 'order_id' : allocated_order_id, 'recipe' : orders[allocated_order_id].recipe }
    return jsonify(response)

@app.route('/factory/orders/<int:order_id>', methods=['PUT'])
def update_order_status(order_id):
    if not order_id in orders:
        abort(404)
    if not 'status' in request.args.keys():
        abort(400)
        redirect(303)
    orders[order_id].status = request.args['status']
    return jsonify('OK')

def __get_expected_time_to_completion(order_id):
    order_status = orders[order_id].status
    if order_status == 'completed':
        return timedelta(seconds = 0)
    elif order_status == 'in progress':
        return timedelta(seconds = 2)
    else: # order_status == 'pending'
        pending_order_ids = __get_pending_order_ids()
        num_higher_prio_orders = pending_order_ids.index(order_id)
        return timedelta(seconds = 5) * (1 + num_higher_prio_orders)

@app.route('/orders/<int:order_id>/status')
def get_order_status(order_id):
    if not order_id in orders:
        abort(404)
    order_status = orders[order_id].status
    expected_time = __get_expected_time_to_completion(order_id).total_seconds()
    response = { \
                'status' : order_status,
                'expected_time_to_completion' : expected_time
               }
    return jsonify(response)

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-b", "--bind-address", default='localhost', dest="bind_address", help="bind to ip-address/host BIND_ADDRESS")
    (options, args) = parser.parse_args()
    app.run(host=options.bind_address, port=12345, debug=True)
