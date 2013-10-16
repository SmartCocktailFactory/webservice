#!/usr/bin/python
# coding: utf8
from flask import Flask, json, request, Response, abort, redirect
from optparse import OptionParser
from datetime import timedelta
from drink import Drink
from order import Order
from utils import jsonify

app = Flask(__name__)

drinks = { }
drinks['Drink1'] = Drink('Drink1', 'Cuba Libre',              Cola=140, Rum=10, IceCube=1)
drinks['Drink1'].description = r"""The Cuba Libre (/ˈkjuːbə ˈliːbreɪ/; Spanish pronunciation: [ˈkuβa ˈliβɾe], "Free Cuba") is a highball made of cola, lime, and white rum. This highball is often referred to as a Rum and Coke in the United States, Canada, the UK, Ireland, Australia and New Zealand where the lime juice may or may not be included."""
drinks['Drink1'].human_readable_recipe = ["120 mL Cola", "50 mL White rum", "10 mL Fresh lime juice"]

drinks['Drink2'] = Drink('Drink2', 'Gin Tonic',     Vodka=10, Cola=140)
drinks['Drink2'].description = r"""A gin and tonic is a highball cocktail made with gin and tonic water poured over ice. It is usually garnished with a slice or wedge of lime."""
drinks['Drink2'].human_readable_recipe = ["120 mL Tonic", "60 mL Gin"]

drinks['Drink3'] = Drink('Drink3', 'Black Russian', Vodka=30, Cola=120,         IceCube=1)
drinks['Drink3'].description = r"""The Black Russian is a cocktail of vodka and coffee liqueur. It contains either three parts vodka and two parts coffee liqueur, per the Kahlúa bottle's label, or five parts vodka to two parts coffee liqueur, per IBA specified ingredients. Traditionally the drink is made by pouring the vodka over ice cubes or cracked ice in an old-fashioned glass, followed by the coffee liqueur."""
drinks['Drink3'].human_readable_recipe = ["50 mL Vodka", "20 mL Coffee liqueur"]

orders = dict()
order_id = 0

@app.route('/')
def welcome():
    return jsonify('Welcome to the Smart Cocktail Factory')

@app.route('/drinks')
def get_drinks():
    response = [d.to_gui_summary() for d in drinks.values()]
    return jsonify(response)

@app.route('/drinks/<drink_id>')
def get_drink_details(drink_id):
    ensure_drink_exists(drink_id)
    response = drinks[drink_id].to_gui_details()
    return jsonify(response)

@app.route('/orders/<drink_id>', methods=['POST'])
def order_drink(drink_id):
    global order_id
    ensure_drink_exists(drink_id)
    order_id += 1
    orders[order_id] = Order(order_id, drink_id, drinks[drink_id].recipe, 'pending')
    return jsonify(order_id)

@app.route('/admin/orders')
def get_orders():
    if 'status' in request.args:
        selected_orders = [o for o in orders.values() if o.status == request.args['status']]
    else:
        selected_orders = orders.values()
    response = [o.to_factory_details() for o in selected_orders]
    return jsonify(response)

@app.route('/admin/orders/clear', methods=['PUT', 'GET'])
def clear_orders():
    global orders, order_id
    orders = dict()
    order_id = 0
    return jsonify('OK')

@app.route('/factory/orders/next', methods=['POST'])
def get_next_order():
    pending_order_ids = get_pending_order_ids()
    if len(pending_order_ids) == 0:
        return jsonify(dict())
    allocated_order_id = min(pending_order_ids)
    orders[allocated_order_id].status = 'in progress'
    response = { 'order_id' : allocated_order_id, 'recipe' : orders[allocated_order_id].recipe }
    return jsonify(response)

@app.route('/factory/orders/<int:order_id>', methods=['PUT'])
def update_order_status(order_id):
    ensure_order_exists(order_id)
    if not 'status' in request.args.keys():
        abort(400)
    orders[order_id].status = request.args['status']
    return jsonify('OK')

@app.route('/orders/<int:order_id>')
def get_order_status(order_id):
    ensure_order_exists(order_id)
    response = orders[order_id].to_gui_summary()
    response['expected_time_to_completion'] = get_expected_time_to_completion(order_id).total_seconds()
    return jsonify(response)

def get_expected_time_to_completion(order_id):
    order_status = orders[order_id].status
    if order_status == 'completed':
        return timedelta(seconds = 0)
    elif order_status == 'in progress':
        return timedelta(seconds = 2)
    else: # order_status == 'pending'
        pending_order_ids = get_pending_order_ids()
        num_higher_prio_orders = pending_order_ids.index(order_id)
        return timedelta(seconds = 5) * (1 + num_higher_prio_orders)

def ensure_drink_exists(drink_id):
    if not drink_id in drinks.keys():
        abort(404)

def ensure_order_exists(order_id):
    if not order_id in orders.keys():
        abort(404)

def get_order_ids_with_status(status):
    return [o_id for o_id in orders if orders[o_id].status == status]

def get_pending_order_ids():
    return get_order_ids_with_status('pending')


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-b", "--bind-address", default='localhost', dest="bind_address", help="bind to ip-address/host BIND_ADDRESS")
    (options, args) = parser.parse_args()
    app.run(host=options.bind_address, port=12345, debug=True)
