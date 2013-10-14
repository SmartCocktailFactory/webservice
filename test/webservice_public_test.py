import os
import webservice
import unittest
import tempfile
import json

class WebservicePublicTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, webservice.app.config['DATABASE'] = tempfile.mkstemp()
        webservice.app.config['TESTING'] = True
        self.app = webservice.app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(webservice.app.config['DATABASE'])

    def get_response(self, uri):
        response = self.app.get(uri)
        jsonResponse = json.loads(response.data)
        return jsonResponse

    def test_getIndex(self):
        expected = 'Welcome to the Smart Cocktail Factory'
        self.assertEqual(expected, self.get_response('/'))

    def test_getDrinks(self):
        response = self.get_response('/drinks')
        self.assertEqual(list, type(response))
        self.assertEqual(4, len(response))

if __name__ == '__main__':
    unittest.main()
