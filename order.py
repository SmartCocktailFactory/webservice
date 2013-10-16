class Order(object):

    def __init__(self, order_id, drink_id, recipe, status):
        self.order_id = order_id
        self.drink_id = drink_id
        self.recipe = recipe
        self.status = status

    def to_factory_details(self):
        return \
        {
              'order_id' : self.order_id,
              'drink_id' : self.drink_id,
              'recipe' : self.recipe,
              'status' : self.status
        }
