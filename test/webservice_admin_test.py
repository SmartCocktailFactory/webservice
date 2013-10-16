import unittest
from webservice_test_facade import WebserviceTestFacade

class WebserviceAdminTestCase(unittest.TestCase):

    def setUp(self):
        self.app = WebserviceTestFacade()
        self.app.clear_orders()

    def test_getOrdersWithNoPendingOrder(self):
        # when
        response = self.app.get_order_list()
        # then
        self.assertTrue(dict, type(response))
        self.assertEquals(0, len(response['orders']))

    def test_getOrdersWithPendingOrders(self):
        # given
        self.app.order_drink()
        self.app.order_drink()
        # when
        response = self.app.get_order_list()
        # then
        self.assertTrue(dict, type(response))
        self.assertEquals(2, len(response['orders']))
