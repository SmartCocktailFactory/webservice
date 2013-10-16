
class Drink(object):

    def __init__(self, id, drink_name):
        self.id = id
        self.name = drink_name
        self.recipe = dict()
        self.description = ''
        self.human_readable_recipe = []

    def to_gui_summary(self):
        return \
        {
                'id' : self.id,
                'name' : self.name
        }

    def to_gui_details(self):
        return \
        {
                'id' : self.id,
                'name' : self.name,
                'description' : self.description,
                'recipe' : self.human_readable_recipe
        }

