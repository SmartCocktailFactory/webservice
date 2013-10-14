import webservice
import unittest
import json

class WebservicePublicTestCase(unittest.TestCase):

    def setUp(self):
        webservice.app.config['TESTING'] = True
        self.app = webservice.app.test_client()

    def tearDown(self):
        pass #empty

    def get(self, uri):
        response = self.app.get(uri)
        jsonResponse = json.loads(response.data)
        return jsonResponse

    def put(self, uri):
        response = self.app.put(uri)
        jsonResponse = json.loads(response.data)
        return jsonResponse

    def test_getIndex(self):
        expected = 'Welcome to the Smart Cocktail Factory'
        self.assertEqual(expected, self.get('/'))

    def test_getDrinks(self):
        response = self.get('/drinks')
        self.assertEqual(list, type(response))
        self.assertEqual(4, len(response))

    def test_orderDrink(self):
        response = self.put('/orders/Martini')
        self.assertEquals(int, type(response))
        response_next = self.put('/orders/Martini')
        self.assertEquals(response_next, response + 1)

    def test_orderDrinkThenCheckOrders(self):
        #given
        ordersResponseOld = self.get('/orders')
        # when
        self.put('/orders/Martini')
        ordersResponseNew = self.get('/orders')
        #then
        self.assertEquals(len(ordersResponseOld) + 1, len(ordersResponseNew))

if __name__ == '__main__':
    unittest.main()
