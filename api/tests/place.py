import unittest
import json
import logging
from app import app
from app.views import *
from app.models.place import Place
from app.models.user import User
from app.models.state import State
from app.models.city import City
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
        database.create_tables([User, City, Place, State])

        '''Create items in tables for ForeignKeyField requirements'''
        self.app.post('/states', data=dict(name="test"))
        self.app.post('/states/1/cities', data=dict(
            name="test",
            state=1
        ))
        self.app.post('/users', data=dict(
            first_name="test",
            last_name="test",
            email="test",
            password="test"
        ))

    def tearDown(self):
        '''Drops the state and city tables.'''
        database.drop_tables([User, City, Place, State])

    def create_place(self, route, name_param):
        '''Makes a post request with the parameters in dict. This adds a city
        to the table City. These last three params are necessary to suppress
        warnings that there is no default value for the field.

        Keyword arguments:
        city_name -- The required name of the city.
        '''
        return self.app.post(route, data=dict(
            owner=1,
            city=1,
            name="test",
            description="test",
            latitude=0,
            longitude=0
        ))

    def test_create(self):
        for i in range(1, 3):
            res = self.create_place('/places', 'test_' + str(i))

            '''The dictionary returns an object with the correct id.'''
            self.assertEqual(json.loads(res.data).get('id'), i)

    def test_create_id(self):
        for i in range(1, 3):
            res = self.create_place('/places', 'test_' + str(i))

        res = self.app.get('/places/2')

        '''The dictionary returns an object with the correct id.'''
        self.assertEqual(json.loads(res.data).get('id'), 2)

        '''Update the id of the item.'''
        self.app.put('/places/2', data=dict(name='updated_data'))
        res = self.app.get('/places/2')
        self.assertEqual(json.loads(res.data).get('name'), 'updated_data')

        '''You may not update the owner.'''
        res = self.app.put('/places/1', data=dict(owner="test"))
        self.assertEqual(res.status_code, 409)

        '''You may not update the city.'''
        res = self.app.put('/places/1', data=dict(city="test"))
        self.assertEqual(res.status_code, 409)

    def test_delete(self):
        for i in range(1, 3):
            self.create_place('/places', 'test_' + str(i))

        '''Delete place with the id 2.'''
        self.app.delete('/places/2')

        '''There is only one remaining place in the table, that with id 1.'''
        res = self.app.get('/places')
        self.assertEqual(len(json.loads(res.data)), 1)
        self.assertEqual(json.loads(res.data)[0].get('id'), 1)

    def test_get_places_by_id(self):
        for i in range(1, 3):
            self.create_place('/places', 'test_' + str(i))
        res = self.app.get('/states/1/cities/1/places')
        self.assertEqual(len(json.loads(res.data)), 2)

        '''Test creation of place in this city and state.'''
        res = self.app.post('/states/1/cities/1/places', data=dict(
            owner=1,
            city=1,
            name="test",
            description="test",
            latitude=0,
            longitude=0
        ))
        res = self.app.get('/states/1/cities/1/places')
        self.assertEqual(len(json.loads(res.data)), 3)

if __name__ == '__main__':
    unittest.main()
