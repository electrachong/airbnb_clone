import unittest
import json
import logging
from app import app
from app.views import *
from app.models.place_book import PlaceBook
from app.models.city import City
from app.models.place import Place
from app.models.user import User
from app.models.state import State
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
        database.create_tables([User, State, City, Place, PlaceBook])

        '''Create table items for ForeignKeyField requirements.'''
        self.app.post('/users', data=dict(
            first_name="test",
            last_name="test",
            email="test",
            password="test"
        ))

        self.app.post('/states', data=dict(name="test"))

        self.app.post('/states/1/cities', data=dict(
            name="test",
            state=1
        ))

        self.app.post('/places', data=dict(
            owner=1,
            city=1,
            name="test",
            description="test",
            latitude=0,
            longitude=0
        ))

    def tearDown(self):
        '''Drops the state and city tables.'''
        database.drop_tables([User, State, City, Place, PlaceBook])

    def create_placebook(self, route, datetime_string, desc):
        '''Makes a post request with the parameters in dict. This adds a city
        to the table City. These last three params are necessary to suppress
        warnings that there is no default value for the field.

        Keyword arguments:
        route -- The route of the request.
        date_start_param -- The date of the book start. Must take the format
        "%Y/%m/%d %H:%M:%S"
        '''
        return self.app.post(route, data=dict(
            place=1,
            user=1,
            date_start=datetime_string,
            description=desc,
            latitude=0,
            longitude=0
        ))

    def test_create(self):
        for i in range(1, 3):
            res = self.create_placebook('/places/1/books',
                                        datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
                                        'test_' + str(i))

            '''The dictionary returns an object with the correct id.'''
            self.assertEqual(json.loads(res.data).get('id'), i)

        res = self.app.get('/places/1/books')
        self.assertEqual(len(json.loads(res.data)), 2)

        '''date_start field must take the form "%Y/%m/%d %H:%M:%S", test
        for this case by giving it an incorrect format (year comes after day
        and month).'''
        res = self.create_placebook('/places/1/books',
                                    '07/21/2016 13:00:16',
                                    'test')

        self.assertEqual(res.status_code, 409)

    def test_create_id(self):
        for i in range(1, 3):
            res = self.create_placebook('/places/1/books',
                                        datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
                                        'test_' + str(i))

        res = self.app.get('/places/1/books/2')
        self.assertEqual(json.loads(res.data).get("id"), 2)

        '''Update the boolean `is_validated` of the book. It is False by
        default.'''
        res = self.app.put('/places/1/books/2', data=dict(
            is_validated=True,
        ))

        res = self.app.get('/places/1/books/2')
        self.assertEqual(json.loads(res.data).get("is_validated"), True)

        '''You may not update the user of a book.'''
        res = self.app.put('/places/2/books/2', data=dict(
            user=2,
        ))
        self.assertEqual(res.status_code, 409)

    def test_delete(self):
        for i in range(1, 3):
            res = self.create_placebook('/places/1/books',
                                        datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
                                        'test_' + str(i))
        '''Delete book with the id 1.'''
        self.app.delete('/places/1/books/1')

        '''There is only one remaining booking in the table, that with id 2.'''
        res = self.app.get('/places/1/books')
        self.assertEqual(len(json.loads(res.data)), 1)
        self.assertEqual(json.loads(res.data)[0].get('id'), 2)


if __name__ == '__main__':
    unittest.main()
