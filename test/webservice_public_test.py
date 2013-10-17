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
        self.assertEqual(dict, type(response))
        self.assertEqual(8, len(response['drinks']))
        for d in response['drinks']:
            self.assertTrue(dict, type(d))
            self.assertTrue('id' in d.keys())
            self.assertTrue('name' in d.keys())

    def test_getDrinkDetails(self):
        # when
        response = self.app.get_drink_details()
        # then
        self.assertEquals(dict, type(response))
        self.assertTrue('id' in response.keys())
        self.assertTrue('name' in response.keys())
        self.assertTrue('description' in response.keys())
        self.assertTrue('recipe' in response.keys())

    def test_getDrinkDetailsForInexistantDrink(self):
        try:
            self.app.get_drink_details('ADrinkThatDoesNotExist')
        except WebApplicationError as error:
            if error.status_code != 404:
                self.fail("Drink does not exist. application should report 404")
        else:
            self.fail("Drink does not exist. application should report error.")

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
        # given
        drinks = self.app.get_drink_list()
        drink_list = drinks['drinks']
        response = 0
        # when
        for drink_summary in drink_list:
            response = self.app.order_drink(drink_summary['id'])
        # then
        self.assertEquals(len(drink_list), response)

    def test_orderDrinkThatDoesNotExist(self):
        try:
            self.app.order_drink('ADrinkThatDoesNotExist')
        except WebApplicationError as error:
            if error.status_code != 404:
                self.fail("Drink does not exist. application should report 404")
        else:
            self.fail("Drink does not exist. application should report error.")

    def test_getOrderStatusForPending(self):
        # given
        drink_id = self.app.default_drink_id
        self.app.order_drink(drink_id)
        # when
        response = self.app.get_order_status(1)
        # then
        self.assertEquals(dict, type(response))
        self.assertEquals('pending', response['status'])
        self.assertTrue(response['expected_time_to_completion'] > 0)
        self.assertEqual(drink_id, response['drink_id'])

    def test_getOrderStatusForInProgress(self):
        # given
        drink_id = self.app.default_drink_id
        self.app.order_drink(drink_id)
        self.app.read_next_order()
        # when
        response = self.app.get_order_status(1)
        # then
        self.assertEquals(dict, type(response))
        self.assertEquals('in progress', response['status'])
        self.assertTrue(response['expected_time_to_completion'] > 0)
        self.assertEqual(drink_id, response['drink_id'])

    def test_getOrderStatusForCompleted(self):
        # given
        drink_id = self.app.default_drink_id
        self.app.order_drink(drink_id)
        self.app.read_next_order()
        self.app.set_order_completed(1)
        # when
        response = self.app.get_order_status(1)
        # then
        self.assertEquals(dict, type(response))
        self.assertEquals('completed', response['status'])
        self.assertTrue(response['expected_time_to_completion'] == 0)
        self.assertEqual(drink_id, response['drink_id'])


if __name__ == '__main__':
    unittest.main()
