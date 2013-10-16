import unittest
from webservice_test_facade import WebserviceTestFacade, WebApplicationError

class WebservicePublicTestCase(unittest.TestCase):

    def setUp(self):
        self.app = WebserviceTestFacade()
        self.app.clear_orders()

    def test_getIndex(self):
        # when
        response = self.app.get_index()
        # then
        self.assertEqual('Welcome to the Smart Cocktail Factory', response)

    def test_getDrinks(self):
        # when
        response = self.app.get_drink_list()
        # then
        self.assertEqual(list, type(response))
        self.assertEqual(3, len(response))

    def test_orderDrink(self):
        # when
        response = self.app.order_drink()
        # then
        self.assertEquals(int, type(response))
        self.assertEquals(1, response)

    def test_orderDrinkJustAnotherDrink(self):
        # given
        self.app.order_drink()
        # when
        response = self.app.order_drink()
        # then
        self.assertEquals(2, response)

    def test_orderDrinkAllAvailableDrinks(self):
        #given
        drinks = self.app.get_drink_list()
        #when
        response = 0
        for drink_id in drinks:
            response = self.app.order_drink(drink_id)
        self.assertEquals(len(drinks), response)

    def test_orderDrinkThatDoesNotExist(self):
        try:
            self.app.order_drink('ADrinkThatDoesNotExist')
        except WebApplicationError as error:
            if error.status_code != 404:
                self.fail("Drink does not exist. application should report 404")
        else:
            self.fail("Drink does not exist. application should report error.")

if __name__ == '__main__':
    unittest.main()
