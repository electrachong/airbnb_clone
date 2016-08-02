import unittest
import json
import logging
from app import app
from app.models.user import User
from app.models.base import database
from flask_json import JsonTestResponse
from peewee import *

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        logging.disable(logging.CRITICAL)
        self.app.response_class = JsonTestResponse
        self.client = self.app.test_client()
        database.create_tables([User], safe=True)

    def tearDown(self):
        database.drop_table(User)

    def post_data(self, route, **data):
        data_list = {
            'first_name': "John",
            'last_name': "Smith",
            'email': "js@number",
            'password': "opensesame" 
        }
        for key, value in data.iteritems():
            data_list[key] = value

        return self.client.post(route, data=data_list)

    def test_create(self):
        #test response for code 201
        assert self.post_data("/users").status_code == 201, (
            "Failed to create new user and return code 201"
        )
        #test for primary key auto-incrementing   
        for i in range(2, 4):
            res = self.post_data("/users", email=i)
            assert res.json['id'] == (i), (
                "Status Code is NOT 201, or primary key is not incrementing"
            )
    
        #test for unique email enforcement
        assert self.post_data("/users", email=i).status_code == 409, (
            "Status Code is NOT 201, or does not exist"
        )

    def test_list(self):
        assert self.post_data("/users", first_name=None).json['code'] == 10000, (
            "Response should NOT return an element on failure"
            )
        try:
            self.post_data("/users").json['created_at']
        except KeyError:
            raise AssertionError("Respondse should return an element on failure")

    def test_get(self):
        new_user = self.post_data("/users").json
        user_get = self.client.get("/users/" + str(new_user['id']))
        assert user_get.status_code == 200, (
            "Get user by ID failed"
        )
        assert len(new_user) == len(set(new_user) & set(user_get.json)), (
            "Respondse data from post and get do not match"
        )
        assert self.client.get("/users/10").status_code == 404, (
            "Unknown user must return with 404"
        )

    def test_delete(self):
        new_user = self.post_data("/users").json
        pre_count = len(self.client.get("/users").json)
        eulogy = self.client.delete("/users/" + str(new_user['id']))
        post_count = len(self.client.get("/users").json)

        assert eulogy.status_code == 200, (
            "Delete user by ID is NOT returning code 200"
        )
        assert post_count == pre_count - 1, (
            "Total user count has not changed after delete"
        )
        assert self.client.delete("/users/10").status_code == 404, (
            "Deleting a non existent user should respond with a 404"
        )

    def test_update(self):
        new_user = self.post_data("/users").json
        update_param = "Jane"
        change = self.client.put("/users/" + str(new_user['id']), data={'first_name': update_param})

        assert change.status_code == 201, (
            "Update user by ID is NOT returning code 201"
        )
        assert change.json['first_name'] == update_param, (
            "Put request did not update user properly"
        )
        assert self.client.put("/users/10", 
            data={'first_name': update_param}).status_code == 404, (
            "Updating a non existent user should respond with a 404"
        )

if __name__ == '__main__':
    unittest.main()
