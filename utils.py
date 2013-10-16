from flask import json
from datetime import timedelta
from flask import abort

def jsonify(obj):
    return json.dumps(obj, indent=4, sort_keys=True)

def get_expected_time_to_completion(orders, order_id):
    order_status = orders.get(order_id).status
    if order_status == 'completed':
        return timedelta(seconds = 0)
    elif order_status == 'in progress':
        return timedelta(seconds = 2)
    else: # order_status == 'pending'
        pending_order_ids = [o.order_id for o in orders.get_all_pending()]
        num_higher_prio_orders = pending_order_ids.index(order_id)
        return timedelta(seconds = 5) * (1 + num_higher_prio_orders)

def ensure_drink_exists(drinks, drink_id):
    if not drink_id in drinks.keys():
        abort(404)

def ensure_order_exists(orders, order_id):
    if not orders.has_order_id(order_id):
        abort(404)

