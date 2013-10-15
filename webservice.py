# coding: utf8
from flask import Flask, json, request, Response, abort, redirect
from drink import Drink
from order import Order

app = Flask(__name__)

drinks = [ \
  #                              [Vodka ml]   [Cola ml]    [Rum ml]    [Ice cubes]
    Drink('Drink1', 'Drink 1', [  0,           140,          10,            1 ]),
    Drink('Drink2', 'Drink 2', [  10,          140,           0,            0 ]),
    Drink('Drink3', 'Drink 3', [  30,          120,           0,            1 ]),
]

orders = []
order_id = 0

@app.route('/')
def welcome():
    return __jsonify('Welcome to the Smart Cocktail Factory')

@app.route('/drinks')
def get_drinks():
    return __jsonify([d.drink_id for d in drinks])

@app.route('/orders/<drink_id>', methods=['PUT'])
def order_drink(drink_id):
    global order_id
    if not drink_id in [d.drink_id for d in drinks]:
        abort(404)
    order_id += 1
    orders.append(Order(order_id, drink_id, 'pending'))
    return __jsonify(order_id)

@app.route('/orders')
def get_orders():
    return __jsonify([(o.order_id, o.drink_id, o.status) for o in orders])

@app.route('/factory/orders/next', methods=['PUT'])
def get_next_order():
    allocated_order = orders.iteritems().next()
    allocated_order_id = allocated_order[0]
    orders[allocated_order_id]

def __jsonify(obj):
    return json.dumps(obj, indent=4, sort_keys=True)


if __name__ == '__main__':
    app.run(host='localhost', port=12345, debug=True)
