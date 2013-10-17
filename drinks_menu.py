# coding: utf8
from drink import Drink

def create_drinks_menu():
    drinks = dict()
    d = Drink('ScrewdriverStraight', 'Screwdriver (straight)')
    d.recipe = dict(Vodka=50, OrangeJuice=100)
    d.description = r"""A screwdriver is a popular alcoholic highball drink made with orange juice and vodka. The International Bartender Association has designated this cocktail as an IBA Official Cocktail."""
    d.human_readable_recipe = ["50 mL vodka", "100 mL orange juice"]
    drinks[d.id] = d

    d = Drink('ScrewdriverOtr', 'Screwdriver (on the rocks)')
    d.recipe = dict(Vodka=50, OrangeJuice=100, IceCube=5)
    d.description = r"""A screwdriver is a popular alcoholic highball drink made with orange juice and vodka. The International Bartender Association has designated this cocktail as an IBA Official Cocktail."""
    d.human_readable_recipe = ["50 mL vodka", "100 mL orange juice", "ice cubes"]
    drinks[d.id] = d

    d = Drink('OjStraight', 'Orange Juice (straight)')
    d.recipe = dict(OrangeJuice=150)
    d.description = r"""Orange juice is made by squeezing the fresh fruit, by drying and later rehydrating the juice, or by concentration of the juice and later adding water to the concentrate. It is known for its health benefits, particularly its high concentration of vitamin C. In American English, the slang term O.J. may also be used to refer to orange juice."""
    d.human_readable_recipe = ["150 mL orange juice"]
    drinks[d.id] = d

    d = Drink('OjOtr', 'Orange Juice (on the rocks)')
    d.recipe = dict(OrangeJuice=150, IceCube=5)
    d.description = r"""Orange juice is made by squeezing the fresh fruit, by drying and later rehydrating the juice, or by concentration of the juice and later adding water to the concentrate. It is known for its health benefits, particularly its high concentration of vitamin C. In American English, the slang term O.J. may also be used to refer to orange juice."""
    d.human_readable_recipe = ["150 mL orange juice", "ice cubes"]
    drinks[d.id] = d

    d = Drink('BacardiStraight', 'Bacardi (straight)')
    d.recipe = dict(Bacardi=50)
    d.description = r"""Bacardi Limited (English: /bəˈkɑrdi/; Catalan: [bəkəɾˈði]; Spanish: [bakarˈði]) is the largest privately held, family-owned spirits company in the world. Originally known for its eponymous Bacardi white rum, it's now also known for its brand portfolio comprising more than 200 brands and labels."""
    d.human_readable_recipe = ["50 mL Bacardi rum"]
    drinks[d.id] = d

    d = Drink('BacardiOtr', 'Bacardi (on the rocks)')
    d.recipe = dict(Bacardi=50, IceCube=5)
    d.description = r"""Bacardi Limited (English: /bəˈkɑrdi/; Catalan: [bəkəɾˈði]; Spanish: [bakarˈði]) is the largest privately held, family-owned spirits company in the world. Originally known for its eponymous Bacardi white rum, it's now also known for its brand portfolio comprising more than 200 brands and labels."""
    d.human_readable_recipe = ["50 mL Bacardi rum", "ice cubes"]
    drinks[d.id] = d

    d = Drink('BacardiOrangeStraight', 'Bacardi Orange (straight)')
    d.recipe = dict(Bacardi=50, OrangeJuice=100)
    d.description = r"""A fresh high ball with Bacardi white rum and orange juice."""
    d.human_readable_recipe = ["50 mL Bacardi rum"]
    drinks[d.id] = d

    d = Drink('BacardiOrangeOtr', 'Bacardi Orange (on the rocks)')
    d.recipe = dict(Bacardi=50, OrangeJuice=100, IceCube=5)
    d.description = r"""A fresh high ball with Bacardi white rum and orange juice."""
    d.human_readable_recipe = ["50 mL Bacardi rum", "ice cubes"]
    drinks[d.id] = d

    return drinks