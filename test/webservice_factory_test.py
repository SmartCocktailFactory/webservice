import unittest
from webservice_test_facade import WebserviceTestFacade

class WebserviceFactoryTestCase(unittest.TestCase):

    def setUp(self):
        self.app = WebserviceTestFacade()
        self.app.clear_orders()

    def test_nextOrderWhenNoOrdersArePending(self):
        # when
        response = self.app.read_next_order()
        # then
        self.assertEqual(dict, type(response))
        self.assertEqual(dict(), response)

    def test_nextOrderWhenOneOrderIsPending(self):
        # given
        self.app.order_drink('Drink1')
        # when
        response = self.app.read_next_order()
        # then
        self.assertEqual(dict, type(response))
        self.assertEqual(1, response['order_id'])
        self.assertEqual(dict, type(response['recipe']))

    def test_nextOrderWhenNoOrderIsPendingButOneInProgress(self):
        # given
        self.app.order_drink()
        self.app.read_next_order()
        # when
        response = self.app.read_next_order()
        # then
        self.assertEqual(dict, type(response))
        self.assertEqual(dict(), response)

    def test_pendingOrdersWhenNoOrdersArePending(self):
        # when
        response = self.app.get_pending_orders()
        # then
        self.assertEqual(0, len(response))

    def test_pendingOrdersWhenOneOrderIsPending(self):
        # given
        self.app.order_drink()
        # when
        response = self.app.get_pending_orders()
        # then
        self.assertEqual(list, type(response))
        self.assertEqual(1, len(response))

    def test_pendingOrdersWhenNoOrderIsPendingButOneInProgress(self):
        # given
        self.app.order_drink()
        self.app.read_next_order()
        # when
        response = self.app.get_pending_orders()
        # then
        self.assertEqual(list, type(response))
        self.assertEqual(list(), response)


if __name__ == '__main__':
    unittest.main()
