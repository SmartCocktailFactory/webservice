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
              'recipe' :
                    {
                     'Vodka' : self.recipe[0],
                     'Rum' : self.recipe[1],
                     'Cola' : self.recipe[2],
                     'IceCube' : self.recipe[3],
                    }
        }
        return jsonify(valueObject)
