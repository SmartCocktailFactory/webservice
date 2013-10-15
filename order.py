from utils import jsonify

class Order(object):

    def __init__(self, order_id, drink_id, recipe, status):
        self.order_id = order_id
        self.drink_id = drink_id
        self.recipe = recipe
        self.status = status

    def serializeToJson(self):
        valueObject = \
        {
              'order_id' : self.order_id,
              'drink_id' : self.drink_id,
              'recipe' : self.recipe,
              'status' : self.status
        }
        return jsonify(valueObject)
