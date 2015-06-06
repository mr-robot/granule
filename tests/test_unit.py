__author__ = 'beast'

import unittest, json
from flask import testing

from granule.granular.store import Store

from granule.granular.auth import LDAPAuth

from granule.application import app


class TestFlaskUnit(unittest.TestCase):


    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_get_home(self):
        response = self.app.get("/")

        self.assertEqual(response.status_code, 200)

    def test_get_activities(self):
        response = self.app.get("/api/2015-05-30/activity/")


        self.assertEqual(response.status_code, 401)
        self.assertTrue('WWW-Authenticate' in response.headers)


class TestLDAPAuthUnit(unittest.TestCase):


    def setUp(self):
        self.auth = LDAPAuth('172.17.0.1', port=389, encryption=None, user_dn="cn=%s,dc=example,dc=org", supported_group="group")

    def tearDown(self):
        pass

    def test_setup_ldap(self):
        self.assertIsNotNone(self.auth)


    def test_auth_success(self):

        self.assertTrue(self.auth.authenticate("admin", "admin"))

        self.assertIsNotNone(self.auth)

    def test_auth_failure(self):

        self.assertFalse(self.auth.authenticate("admin", "fail"))

        self.assertIsNotNone(self.auth)

    def test_group_failure(self):

        self.assertFalse(self.auth.check_user_in_group("admin"))

        self.assertIsNotNone(self.auth)

class TestGranuleUnit(unittest.TestCase):


    def setUp(self):

        self.g = Store("172.17.0.1")

    def tearDown(self):
        self.g.r.flushdb()


    def get_user_id(self):

        username = "user_99"
        password = "password_1"

        user_object = self.g.create_user(username, password)

        user_object_loggedin = self.g.login(username, password)

        return user_object_loggedin["user_id"]

    def test_basic_get_activity(self):

        self.get_user_id()

        inputs = json.dumps({"id_a":1})

        activity = {"input": inputs,"id":1}


        result = self.g.run_activity(inputs)

        self.assertIsNotNone(result)

        self.assertEquals(result, 1)

        self.assertEquals(activity, self.g.get_activity(result))



    def test_basic_get_result(self):

        self.get_user_id()

        inputs = json.dumps({"id_a":1})
        results = json.dumps({"result_a":123})

        activity = {"input": inputs,"id":1}
        activity_id = self.g.run_activity(inputs)

        self.g.add_result(activity_id, results)

        activity_with_result = activity
        activity_with_result["result"] = results

        self.assertEquals(activity_with_result, self.g.get_activity(activity_id))


    def test_get_activities(self):

        self.get_user_id()

        inputs = json.dumps({"id_a":1})

        activity_id = self.g.run_activity(inputs)

        activity_id_two = self.g.run_activity(inputs)
        activity_id_three = self.g.run_activity(inputs)

        self.assertEquals([str(activity_id), str(activity_id_two), str(activity_id_three)], self.g.get_all_activities())


    def test_get_user_activities(self):

        user_id = self.get_user_id()

        inputs = json.dumps({"id_a":1})

        activity_id = self.g.run_activity(inputs)

        activity_id_two = self.g.run_activity(inputs)
        activity_id_three = self.g.run_activity(inputs)

        self.assertEquals([str(activity_id), str(activity_id_two), str(activity_id_three)], self.g.get_user_activities(user_id))

    def test_login(self):

        username = "user_1"
        password = "password_1"

        user_object = self.g.create_user(username, password)

        user_object_loggedin = self.g.login(username, password)

        self.assertIsNotNone(user_object)
        self.assertIsNotNone(user_object_loggedin)
        self.assertEquals(user_object, user_object_loggedin)

    def test_create_user(self):

        username = "user_1"
        password = "password_1"

        user_object = self.g.create_user(username, password)

        self.assertIsNotNone(user_object)
        self.assertEquals(user_object["user_id"],'1')


if __name__ == '__main__':
    unittest.main()