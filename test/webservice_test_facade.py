import json
import webservice

class WebserviceTestFacade(object):

    def __init__(self):
        webservice.app.config['TESTING'] = True
        self.__test_client = webservice.app.test_client()
        self.default_drink_id = 'ScrewdriverOtr'

    def get_index(self):
        return self.__get('/')

    def get_drink_list(self):
        return self.__get('/drinks')

    def get_drink_details(self, drink_id='ScrewdriverOtr'):
        return self.__get('/drinks/' + drink_id)

    def order_drink(self, drink_id='ScrewdriverOtr'):
        return self.__post('/orders/' + drink_id)

    def get_order_list(self):
        return self.__get('/admin/orders')

    def get_order_status(self, order_id):
        return self.__get('/orders/' + str(order_id))

    def clear_orders(self):
        return self.__put('/admin/orders/clear')

    def read_next_order(self):
        return self.__post('/factory/orders/next')

    def set_order_completed(self, order_id):
        return self.__put('/factory/orders/' + str(order_id) +'?status=completed')

    def get_pending_orders(self):
        return self.__get('/admin/orders?status=pending')

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
        if response.status_code < 200 or response.status_code >= 300:
            raise WebApplicationError(response.status, response.status_code)
        if type(response.data)==list:
            raise 'response object must be json object, not a list'

class WebApplicationError(Exception):
    def __init__(self, status, status_code):
        self.status = status
        self.status_code = status_code
