#!/usr/bin/python
# coding: utf8
from flask import Flask, json, request, Response, abort, redirect
from optparse import OptionParser
from drinks_menu import create_drinks_menu
from order_queue import OrderQueue
from utils import jsonify, ensure_drink_exists, ensure_order_exists, get_expected_time_to_completion

app = Flask(__name__)

drinks = create_drinks_menu()
orders = OrderQueue()

@app.route('/')
def welcome():
    return jsonify('Welcome to the Smart Cocktail Factory')

@app.route('/drinks')
def get_drinks():
    response = { 'drinks' : [d.to_gui_summary() for d in drinks.values()]}
    return jsonify(response)

@app.route('/drinks/<drink_id>')
def get_drink_details(drink_id):
    ensure_drink_exists(drinks, drink_id)
    response = drinks[drink_id].to_gui_details()
    return jsonify(response)

@app.route('/orders/<drink_id>', methods=['POST'])
def order_drink(drink_id):
    ensure_drink_exists(drinks, drink_id)
    order_id = orders.add(drink_id, drinks[drink_id].recipe)
    return jsonify(order_id)

@app.route('/admin/orders/<drink_id>', methods=['GET'])
def order_drink_admin(drink_id):
    return order_drink(drink_id)

@app.route('/admin/orders')
def get_orders():
    if 'status' in request.args:
        selected_orders = orders.get_all_with_status(request.args['status'])
    else:
        selected_orders = orders.get_all()
    response = { 'orders' : [o.to_admin_details() for o in selected_orders] }
    return jsonify(response)

@app.route('/admin/orders/clear', methods=['PUT', 'GET'])
def clear_orders():
    orders.clear()
    return jsonify('OK')

@app.route('/factory/orders/next', methods=['POST'])
def get_next_order():
    next_pending = orders.pop_next_pending()
    if next_pending is None:
        return jsonify(dict())
    response = next_pending.to_factory_summary()
    return jsonify(response)

@app.route('/factory/orders/<int:order_id>', methods=['PUT'])
def update_order_status(order_id):
    ensure_order_exists(orders, order_id)
    if not 'status' in request.args.keys():
        abort(400)
    orders.get(order_id).status = request.args['status']
    return jsonify('OK')

@app.route('/orders/<int:order_id>')
def get_order_status(order_id):
    ensure_order_exists(orders, order_id)
    response = orders.get(order_id).to_gui_summary()
    response['expected_time_to_completion'] = get_expected_time_to_completion(orders, order_id).total_seconds()
    return jsonify(response)


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-b", "--bind-address", default='localhost', dest="bind_address", help="bind to ip-address/host BIND_ADDRESS")
    (options, args) = parser.parse_args()
    app.run(host=options.bind_address, port=12345, debug=True)
