import unittest
import json
import logging
from app import app
from app.views import *
from app.models.amenity import Amenity
from app.models.base import database
from peewee import *
from datetime import datetime


class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        '''Creates a test client, disables logging, connects to the database
        and creates state and city tables for temporary testing purposes.
        '''
        self.app = app.test_client()
        logging.disable(logging.CRITICAL)
        database.connect()
        database.create_tables([Amenity])

    def tearDown(self):
        '''Drops the state and city tables.'''
        database.drop_tables([Amenity])

    def create_amenity(self, route, amenity_name):
        '''Makes a post request with the parameters in dict. This adds an
        amenity to the table Amenity.

        Keyword arguments:
        route -- The route of the request.
        amenity_name -- The name of the new amenity.
        '''
        return self.app.post(route, data=dict(
            name=amenity_name
        ))

    def test_create(self):
        for i in range(1, 3):
            res = self.create_amenity('/amenities', 'test_' + str(i))

            '''The dictionary returns an object with the correct id.'''
            self.assertEqual(json.loads(res.data).get('id'), i)

        res = self.app.get('/amenities')
        self.assertEqual(len(json.loads(res.data)), 2)

        res = self.create_amenity('/amenities', "test_2")

        '''Do not allow a user to update the name.'''
        self.assertEqual(res.status_code, 409)
        self.assertEqual(json.loads(res.data).get('code'), 10003)

    def test_get_id(self):
        for i in range(1, 3):
            res = self.create_amenity('/amenities', 'test_' + str(i))

        res = self.app.get('/amenities/2')
        self.assertEqual(json.loads(res.data).get("id"), 2)

    def test_delete(self):
        for i in range(1, 3):
            res = self.create_amenity('/amenities', 'test_' + str(i))

        '''Delete amenity with the id 1.'''
        self.app.delete('/amenities/1')

        '''There is only one remaining booking in the table, that with id 2.'''
        res = self.app.get('/amenities')
        self.assertEqual(len(json.loads(res.data)), 1)
        self.assertEqual(json.loads(res.data)[0].get('id'), 2)

'''Add test for the route '/places/1/amenities' whenever POST request
support is added.'''

if __name__ == '__main__':
    unittest.main()
