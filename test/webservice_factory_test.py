import webservice
import unittest
import json

class WebserviceFactoryTestCase(unittest.TestCase):

    def setUp(self):
        webservice.app.config['TESTING'] = True
        self.__test_client = webservice.app.test_client()
        self.put('/factory/orders/clear')

    def tearDown(self):
        pass

    def get(self, uri):
        response = self.__test_client.get(uri)
        jsonResponse = json.loads(response.data)
        return jsonResponse

    def put(self, uri):
        response = self.__test_client.put(uri)
        jsonResponse = json.loads(response.data)
        return jsonResponse

    def test_nextOrderWhenNoOrdersArePending(self):
        #when
        response = self.put('/factory/orders/next')
        #then
        self.assertEqual(dict, type(response))
        self.assertEqual(dict(), response)

    def test_nextOrderWhenOneOrderIsPending(self):
        #given
        self.put('/orders/Drink1')
        #when
        response = self.put('/factory/orders/next')
        #then
        self.assertEqual(dict, type(response))
        self.assertEqual(1, response['order_id'])
        self.assertEqual(dict, type(response['recipe']))

    def test_nextOrderWhenNoOrderIsPendingButOneInProgress(self):
        #given
        self.put('/orders/Drink1')
        self.put('/factory/orders/next')
        #when
        response = self.put('/factory/orders/next')
        #then
        self.assertEqual(dict, type(response))
        self.assertEqual(dict(), response)

    def test_pendingOrdersWhenNoOrdersArePending(self):
        response = self.get('/factory/orders/pending')
        print response
        self.assertEqual(0, len(response))

    def test_pendingOrdersWhenOneOrderIsPending(self):
        #given
        self.put('/orders/Drink1')
        #when
        response = self.get('/factory/orders/pending')
        #then
        self.assertEqual(list, type(response))
        self.assertEqual(1, len(response))

    def test_pendingOrdersWhenNoOrderIsPendingButOneInProgress(self):
        #given
        self.put('/orders/Drink1')
        self.put('/factory/orders/next')
        #when
        response = self.get('/factory/orders/pending')
        #then
        self.assertEqual(list, type(response))
        self.assertEqual(list(), response)


if __name__ == '__main__':
    unittest.main()
