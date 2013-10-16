#!/usr/bin/python
# coding: utf8
from flask import Flask, json, request, Response, abort, redirect
from optparse import OptionParser
from drink import Drink
from order_queue import OrderQueue
from utils import jsonify, ensure_drink_exists, ensure_order_exists, get_expected_time_to_completion

app = Flask(__name__)

drinks = { }
drinks['Drink1'] = Drink('Drink1', 'Cuba Libre')
drinks['Drink1'].recipe = dict(Cola=140, Rum=10, IceCube=1 )
drinks['Drink1'].description = r"""The Cuba Libre (/ˈkjuːbə ˈliːbreɪ/; Spanish pronunciation: [ˈkuβa ˈliβɾe], "Free Cuba") is a highball made of cola, lime, and white rum. This highball is often referred to as a Rum and Coke in the United States, Canada, the UK, Ireland, Australia and New Zealand where the lime juice may or may not be included."""
drinks['Drink1'].human_readable_recipe = ["120 mL Cola", "50 mL White rum", "10 mL Fresh lime juice"]

drinks['Drink2'] = Drink('Drink2', 'Gin Tonic')
drinks['Drink2'].recipe = dict(Vodka=10, Cola=140)
drinks['Drink2'].description = r"""A gin and tonic is a highball cocktail made with gin and tonic water poured over ice. It is usually garnished with a slice or wedge of lime."""
drinks['Drink2'].human_readable_recipe = ["120 mL Tonic", "60 mL Gin"]

drinks['Drink3'] = Drink('Drink3', 'Black Russian')
drinks['Drink3'].recipe = dict(Vodka=30, Cola=120, IceCube=1)
drinks['Drink3'].description = r"""The Black Russian is a cocktail of vodka and coffee liqueur. It contains either three parts vodka and two parts coffee liqueur, per the Kahlúa bottle's label, or five parts vodka to two parts coffee liqueur, per IBA specified ingredients. Traditionally the drink is made by pouring the vodka over ice cubes or cracked ice in an old-fashioned glass, followed by the coffee liqueur."""
drinks['Drink3'].human_readable_recipe = ["50 mL Vodka", "20 mL Coffee liqueur"]

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
