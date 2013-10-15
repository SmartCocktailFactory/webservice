import webservice
import unittest
import json

class WebservicePublicTestCase(unittest.TestCase):

    def setUp(self):
        webservice.app.config['TESTING'] = True
        self.__test_client = webservice.app.test_client()
        self.put('/factory/orders/clear')

    def tearDown(self):
        pass #empty

    def get(self, uri):
        response = self.__test_client.get(uri)
        jsonResponse = json.loads(response.data)
        return jsonResponse

    def put(self, uri):
        response = self.__test_client.put(uri)
        jsonResponse = json.loads(response.data)
        return jsonResponse

    def test_getIndex(self):
        expected = 'Welcome to the Smart Cocktail Factory'
        self.assertEqual(expected, self.get('/'))

    def test_getDrinks(self):
        response = self.get('/drinks')
        self.assertEqual(list, type(response))
        self.assertEqual(3, len(response))

    def test_orderDrink(self):
        response = self.put('/orders/Drink1')
        self.assertEquals(int, type(response))
        response_next = self.put('/orders/Drink1')
        self.assertEquals(response_next, response + 1)

    def test_orderDrinkThenCheckOrders(self):
        #given
        ordersResponseOld = self.get('/orders')
        # when
        self.put('/orders/Drink1')
        ordersResponseNew = self.get('/orders')
        #then
        self.assertEquals(len(ordersResponseOld) + 1, len(ordersResponseNew))

if __name__ == '__main__':
    unittest.main()
