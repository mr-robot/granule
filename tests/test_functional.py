__author__ = 'beast'

import unittest
import requests
import json

class TestRestFunctionalGranule(unittest.TestCase):


    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_basic_rest_functional(self):
        #API calls End point using Basic Auth
        payload = {'some': 'data'}
        response = requests.post("http://localhost:8080/api/2015-05-30/activity/", data=json.dumps(payload))

        #API Gets endpoint response

        self.assertEquals(response.status_code, 200)

        #Endpoint response includes activity details

        #API Gets Activity result Endpoint
        pass


class TestWebFunctionalGranule(unittest.TestCase):


    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_basic_web_test_functional(self):
        #User goes to page, and is asked to Login

        #User Gets redirected to Home page on login

        #User Enters Item Details into Activity Form

        #User Gets result


        pass



if __name__ == '__main__':
    unittest.main()