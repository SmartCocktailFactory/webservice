from order import Order

class OrderQueue(object):

    def __init__(self):
        self.clear()

    def add(self, drink_id, recipe, ):
        self.order_id += 1
        self.orders[self.order_id] = Order(self.order_id, drink_id, recipe, 'pending')
        return self.order_id

    def remove(self, order_id):
        self.orders[order_id] = None

    def clear(self):
        self.order_id = 0
        self.orders = dict()

    def has_order_id(self, order_id):
        return order_id in self.orders.keys()

    def get(self, order_id):
        return self.orders[order_id]

    def get_all(self):
        return self.orders.values()

    def get_all_pending(self):
        return self.get_all_with_status('pending')

    def get_all_in_progress(self):
        return self.get_all_with_status('in progress')

    def get_all_completed(self):
        return self.get_all_with_status('completed')

    def get_all_with_status(self, status):
        return [o for o in self.orders.values() if o.status == status]

    def pop_next_pending(self):
        pending_orders = self.get_all_pending()
        if len(pending_orders) == 0:
            return None
        next_order_id = min([o.order_id for o in pending_orders])
        pending_order = self.orders[next_order_id]
        pending_order.status = 'in progress'
        return pending_order
