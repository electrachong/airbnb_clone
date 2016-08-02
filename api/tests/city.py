import unittest
import json
import logging
from app import app
from app.views import *
from app.models.city import City
from app.models.state import State
from app.models.base import database
from peewee import *


class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        '''Creates a test client, disables logging, connects to the database
        and creates state and city tables for temporary testing purposes.
        '''
        self.app = app.test_client()
        logging.disable(logging.CRITICAL)
        database.connect()
        database.create_tables([State, City])

        '''Create a state for routing purposes.'''
        self.app.post('/states', data=dict(name="test"))

    def tearDown(self):
        '''Drops the state and city tables.'''
        database.drop_tables([State, City])

    def create_city(self, city_name):
        '''Makes a post request with the parameters in dict. This adds a city
        to the table City.

        Keyword arguments:
        city_name -- The required name of the city.
        '''
        return self.app.post('/states/1/cities', data=dict(
            name=city_name,
            state=1
        ))

    def test_create(self):
        for i in range(1, 3):
            res = self.create_city("test_" + str(i))
            '''The dictionary returns an object with the correct id.'''
            self.assertEqual(json.loads(res.data).get("id"), i)

        lacking_param = self.app.post('/states/1/cities',
                                      data=dict(bad_param="test"))
        non_unique_name = self.create_city("test_2")

        self.assertEqual(lacking_param.status_code, 400)
        self.assertEqual(non_unique_name.status_code, 409)

        '''Returned object has the code 10002.'''
        self.assertEqual(json.loads(non_unique_name.data).get("code"), 10002)

    def test_list(self):
        res = self.app.get('/states/1/cities')
        self.assertEqual(len(json.loads(res.data)), 0)

        '''Add one city to database.'''
        res = self.create_city("test")
        res = self.app.get('/states/1/cities')
        self.assertEqual(len(json.loads(res.data)), 1)

    def test_create_with_id(self):
        for i in range(1, 3):
            res = self.create_city("test_" + str(i))

        '''The application returns an object with the correct id.'''
        res = self.app.get('/states/1/cities/2')
        self.assertEqual(json.loads(res.data).get("id"), 2)

    def test_delete(self):
        for i in range(1, 3):
            res = self.create_city("test_" + str(i))

        '''The application deletes an object with the correct id.'''
        res = self.app.delete('/states/1/cities/1')
        self.assertEqual(res.status_code, 200)

        '''The remaining city has an id of 2 because 1 has been deleted.'''
        res = self.app.get('/states/1/cities')
        self.assertEqual(json.loads(res.data)[0].get("id"), 2)

if __name__ == '__main__':
    unittest.main()
