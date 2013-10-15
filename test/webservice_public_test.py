import unittest
from webservice_test_facade import WebserviceTestFacade

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

    def test_orderAnotherDrink(self):
        # given
        response = self.app.order_drink()
        # when
        response_next = self.app.order_drink()
        # then
        self.assertEquals(response_next, response + 1)

    def test_getOrdersWithNoPendingOrder(self):
        # when
        response = self.app.get_order_list()
        # then
        self.assertEquals(0, len(response))

    def test_getOrdersWithPendingOrders(self):
        # given
        self.app.order_drink()
        self.app.order_drink()
        #when
        response = self.app.get_order_list()
        # then
        self.assertEquals(2, len(response))


if __name__ == '__main__':
    unittest.main()
