# coding: utf8
from flask import Flask, json, request, Response, abort, redirect
from functools import wraps

app = Flask(__name__)

cocktails = {
    'Whiskey Sour' : ['4 cl Whiskey', '2 cl Zitronensirup', '1 cl Zitronensaft', '1 Cocktail Kirsche', 'Eiswürfel'], \
    'Cuba Libre' : ['1 Schuss Cola zum Auffüllen', '1 Stück Limette', '4 cl weisser Rum', 'Eiswürfel'], \
    'Martini' : ['4 cl Gin', '1 Olive', '1 cl Vermouth dry', 'Eis'], \
    'Wodka Lemon' : ['1 Schuss Bitter Lemon', '1 Limettenscheibe', '1 cl Limettensaft', '4 cl Wodka', 'Eiswürfel'], \
}

users = {
    'admin' : 'password',
    'abt' : '6655'
}

order_id = 0

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username in users and password == users[username]

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def welcome():
    return 'Welcome to the Smart Cocktail Factory'

@app.route('/cocktails')
@requires_auth
def get_cocktails():
    return json.dumps(cocktails.keys())

@app.route('/cocktails/<cocktail>/recipe')
@requires_auth
def get_recipe(cocktail):
    if not cocktail in cocktails:
        abort(404)
    return json.dumps(cocktails[cocktail])

@app.route('/cocktails/<cocktail>/order', methods=['GET', 'POST'])
def order_drink(cocktail): # TODO add @requires_auth
    global order_id
    if not cocktail in cocktails:
        abort(404)
    if request.method=='GET':
        return "Send a POST to issue an order for this cocktail"
    else:
        # TODO order cocktail
        order_id += 1
        return str(order_id) # order id

@app.route('/signin', methods=['GET', 'POST'])
def sign_in():
    return json.dumps(request.form)
    username = request.form['Username']
    password = request.form['Password']
    if is_valid_new_login(username, password):
        create_login(username, password)
        return "Success"
    else:
        return "Username already taken."

def is_valid_new_login(username, password):
    return not username or username not in users

def create_login(username, password):
    users[username] = password

if __name__ == '__main__':
    app.run(port=12345, debug=True)
