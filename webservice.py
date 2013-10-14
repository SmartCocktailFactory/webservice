# coding: utf8
from flask import Flask, json, request, Response, abort, redirect

app = Flask(__name__)

drinks = {
    'Whiskey Sour' : ['4 cl Whiskey', '2 cl Zitronensirup', '1 cl Zitronensaft', '1 Cocktail Kirsche', 'Eiswürfel'], \
    'Cuba Libre' : ['1 Schuss Cola zum Auffüllen', '1 Stück Limette', '4 cl weisser Rum', 'Eiswürfel'], \
    'Martini' : ['4 cl Gin', '1 Olive', '1 cl Vermouth dry', 'Eis'], \
    'Wodka Lemon' : ['1 Schuss Bitter Lemon', '1 Limettenscheibe', '1 cl Limettensaft', '4 cl Wodka', 'Eiswürfel'], \
}

orders = dict()
order_id = 0

@app.route('/')
def welcome():
    return 'Welcome to the Smart Cocktail Factory'

@app.route('/drinks')
def get_drinks():
    return json.dumps(drinks.keys())

@app.route('/orders/<drink_id>', methods=['PUT'])
def order_drink(drink_id):
    global order_id
    if not drink_id in drinks:
        abort(404)
    else:
        order_id += 1
        orders[order_id] = { 'drink_id' : drink_id, 'status' : 'pending' }
        return json.dumps(order_id)

@app.route('/orders')
def get_orders():
    return json.dumps(orders)

if __name__ == '__main__':
    app.run(host='localhost', port=12345, debug=True)
