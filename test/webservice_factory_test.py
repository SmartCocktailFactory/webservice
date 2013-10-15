import webservice
import unittest
import json

class WebserviceFactoryTestCase(unittest.TestCase):

    def setUp(self):
        webservice.app.config['TESTING'] = True
        self.app = webservice.app.test_client()

    def tearDown(self):
        pass

    def get(self, uri):
        response = self.app.get(uri)
        jsonResponse = json.loads(response.data)
        return jsonResponse

    def put(self, uri):
        response = self.app.put(uri)
        jsonResponse = json.loads(response.data)
        return jsonResponse

    def put_response(self, uri):
        response = self.app.put(uri)
        jsonResponse = json.loads(response.data)
        return jsonResponse

    def test_nextOrder(self):
        response = self.put_response('factory/orders/next')
        self.assertEqual(tuple, type(response))
        self.assertEqual(4, len(response))

if __name__ == '__main__':
    unittest.main()
