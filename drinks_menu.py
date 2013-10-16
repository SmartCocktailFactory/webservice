# coding: utf8
from drink import Drink

def create_drinks_menu():
    drinks = dict()
    drinks['Drink1'] = Drink('Drink1', 'Cuba Libre')
    drinks['Drink1'].recipe = dict(Cola=140, Rum=10, IceCube=1 )
    drinks['Drink1'].description = r"""The Cuba Libre (/ˈkjuːbə ˈliːbreɪ/; Spanish pronunciation: [ˈkuβa ˈliβɾe], "Free Cuba") is a highball made of cola, lime, and white rum. This highball is often referred to as a Rum and Coke in the United States, Canada, the UK, Ireland, Australia and New Zealand where the lime juice may or may not be included."""
    drinks['Drink1'].human_readable_recipe = ["120 mL Cola", "50 mL White rum", "10 mL Fresh lime juice"]

    drinks['Drink2'] = Drink('Drink2', 'Gin Tonic')
    drinks['Drink2'].recipe = dict(Vodka=10, Cola=140)
    drinks['Drink2'].description = r"""A gin and tonic is a highball cocktail made with gin and tonic water poured over ice. It is usually garnished with a slice or wedge of lime."""
    drinks['Drink2'].human_readable_recipe = ["120 mL Tonic", "60 mL Gin"]

    drinks['Drink3'] = Drink('Drink3', 'Black Russian')
    drinks['Drink3'].recipe = dict(Vodka=30, Cola=120, IceCube=1)
    drinks['Drink3'].description = r"""The Black Russian is a cocktail of vodka and coffee liqueur. It contains either three parts vodka and two parts coffee liqueur, per the Kahlúa bottle's label, or five parts vodka to two parts coffee liqueur, per IBA specified ingredients. Traditionally the drink is made by pouring the vodka over ice cubes or cracked ice in an old-fashioned glass, followed by the coffee liqueur."""
    drinks['Drink3'].human_readable_recipe = ["50 mL Vodka", "20 mL Coffee liqueur"]
    return drinks