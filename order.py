class Order(object):

    def __init__(self, order_id, drink_id, drink_name, recipe, status):
        self.order_id = order_id
        self.drink_id = drink_id
        self.drink_name = drink_name
        self.recipe = recipe
        self.status = status

    def to_admin_details(self):
        return \
        {
              'order_id' : self.order_id,
              'drink_id' : self.drink_id,
              'drink_name' : self.drink_name,
              'recipe' : self.recipe,
              'status' : self.status
        }

    def to_factory_summary(self):
        return \
        {
              'order_id' : self.order_id,
              'drink_name' : self.drink_name,
              'recipe' : self.recipe
        }

    def to_gui_summary(self):
        return \
        {
              'drink_id' : self.drink_id,
              'status' : self.status,
              'expected_time_to_completion' : 0
        }
