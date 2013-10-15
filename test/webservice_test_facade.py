import json
import webservice

class WebserviceTestFacade(object):

    def __init__(self):
        webservice.app.config['TESTING'] = True
        self.__test_client = webservice.app.test_client()

    def get_index(self):
        return self.__get('/')

    def get_drink_list(self):
        return self.__get('/drinks')

    def order_drink(self, drink_id='Drink1'):
        return self.__put('/orders/' + drink_id)

    def get_order_list(self):
        return self.__get('/orders')

    def clear_orders(self):
        return self.__put('/factory/orders/clear')

    def read_next_order(self):
        return self.__put('/factory/orders/next')

    def get_pending_orders(self):
        return self.__get('/factory/orders/pending')

    def __get(self, uri):
        response = self.__test_client.get(uri)
        jsonResponse = json.loads(response.data)
        return jsonResponse

    def __put(self, uri):
        response = self.__test_client.put(uri)
        jsonResponse = json.loads(response.data)
        return jsonResponse
