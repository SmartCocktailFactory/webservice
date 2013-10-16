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
        return self.__post('/orders/' + drink_id)

    def get_order_list(self):
        return self.__get('/admin/orders')

    def clear_orders(self):
        return self.__put('/admin/orders/clear')

    def read_next_order(self):
        return self.__post('/factory/orders/next')

    def get_pending_orders(self):
        return self.__get('/factory/orders/pending')

    def __get(self, uri):
        response = self.__test_client.get(uri)
        self.__ensure_response_is_ok(response)
        jsonResponse = json.loads(response.data)
        return jsonResponse

    def __post(self, uri):
        response = self.__test_client.post(uri)
        self.__ensure_response_is_ok(response)
        jsonResponse = json.loads(response.data)
        return jsonResponse

    def __put(self, uri):
        response = self.__test_client.put(uri)
        self.__ensure_response_is_ok(response)
        jsonResponse = json.loads(response.data)
        return jsonResponse

    def __ensure_response_is_ok(self, response):
        if response.status_code >= 200 and response.status_code < 300:
            raise WebApplicationError(response.status, response.status_code)

class WebApplicationError(Exception):
    def __init__(self, status, status_code):
        self.status = status
        self.status_code = status_code
