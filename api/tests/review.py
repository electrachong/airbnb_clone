import unittest
import json
import logging
from app import app
from app.views import *
from app.models.user import User
from app.models.review import Review
from app.models.review_user import ReviewUser
from app.models.place import Place
from app.models.review_place import ReviewPlace
from app.models.city import City
from app.models.state import State
from app.models.base import BaseModel
from peewee import *


class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        '''Creates a test client, disables logging, connects to the database
        and creates a table User for temporary testing purposes.
        '''
        self.app = app.test_client()
        logging.disable(logging.CRITICAL)
        BaseModel.database.connect()
        BaseModel.database.create_tables([User, Place, Review, ReviewPlace,
                                          ReviewUser, City, State])

        '''Add two new users.'''
        for i in range(1, 3):
            self.app.post('/users', data=dict(first_name="user_" + str(i),
                                              last_name="user_" + str(i),
                                              email="user_" + str(i),
                                              password="user_" + str(i)))

        '''Add a state.'''
        self.app.post('/states', data=dict(name="state_1"))

        '''Add a city.'''
        self.app.post('/states/1/cities', data=dict(name="city_1", state=1))

        '''Add a place.'''
        self.app.post('/places', data=dict(owner=1, city=1, name="place_1",
                                           description="place_1", latitude=0,
                                           longitude=0))

    def tearDown(self):
        '''Drops the table User.'''
        BaseModel.database.drop_tables([User, Place, Review, ReviewPlace,
                                        ReviewUser, City, State])

    def create_review(self, route, message_str, user_id):
        '''Makes a post request with the parameters in dict. Essentially this
        adds a user to the table User.

        Keyword arguments:
        first -- The required first name of the user.
        **op -- An optional argument (e.g., "pw") for testing purposes.
        '''
        return self.app.post(route, data=dict(
            message=message_str,
            user=user_id
        ))

    def test_get_reviews(self):
        res = self.app.get('/users/2/my_reviews')

        '''The length of a user with no reviews should be 0.'''
        self.assertEqual(len(json.loads(res.data)), 0)
        self.create_review('/users/1/reviews', 'test', 2)

        '''After creating a new review of user 2, the length should be 1.'''
        res = self.app.get('/users/2/my_reviews')
        self.assertEqual(len(json.loads(res.data)), 1)

        '''Query for an unknown user id number should return 404 status.'''
        res = self.app.get('/users/3/reviews')
        self.assertEqual(res.status_code, 404)

    def test_post_reviews(self):
        '''Query for an unknown user id number should return 404 status.'''
        res = self.create_review('/users/3/reviews', 'test', 2)
        self.assertEqual(res.status_code, 404)

        '''Create the review corretly when all parameters are passed.'''
        for i in range(1, 3):
            res = self.create_review('/users/1/reviews', 'test', 2)
            self.assertEqual(json.loads(res.data).get('touserid'), 1)
            self.assertEqual(json.loads(res.data).get('fromuserid'), 2)
            self.assertEqual(json.loads(res.data).get('id'), i)

        '''Test for a cases where required parameters are missing or improper
        types are passed as parameter (e.g., an string instead of an int).'''
        missing_message = self.app.post('/users/1/reviews', data=dict(
            user=2
        ))
        missing_user = self.app.post('/users/1/reviews', data=dict(
            message="test"
        ))
        self.assertEqual(missing_message.status_code, 404)
        self.assertEqual(missing_user.status_code, 404)

        '''TODO: Add test for incorrect data types.'''

    def test_list(self):
        '''Create two reviews from user 2 to user 1.'''
        for i in range(1, 3):
            res = self.create_review('/users/1/reviews', 'test_' + str(i), 2)

        '''This should return the review for the respective users.'''
        res = self.app.get('/users/1/reviews/1')
        self.assertEqual(json.loads(res.data)[0].get('message'), 'test_1')
        res = self.app.get('/users/1/reviews/2')
        self.assertEqual(json.loads(res.data)[0].get('message'), 'test_2')

        '''Test cases where the user or review ids do not exist.'''
        res = self.app.get('/users/3/reviews/1')
        self.assertEqual(res.status_code, 404)
        res = self.app.get('/users/1/reviews/3')
        self.assertEqual(res.status_code, 404)

    def test_delete(self):
        '''Create two reviews from user 2 to user 1.'''
        for i in range(1, 3):
            res = self.create_review('/users/1/reviews', 'test_' + str(i), 2)

        '''Before delete, there are two reviews for user 1.'''
        res = self.app.get('/users/1/reviews')
        self.assertEqual(len(json.loads(res.data)), 2)

        '''Delete review with id 1. Returns 200 status code.'''
        res = self.app.delete('/users/1/reviews/1')
        self.assertEqual(res.status_code, 200)

        '''After delete, there is 1 review for user 1.'''
        res = self.app.get('/users/1/reviews')
        self.assertEqual(len(json.loads(res.data)), 1)

        '''Test cases where the user or review ids do not exist.'''
        res = self.app.delete('/users/3/reviews/1')
        self.assertEqual(res.status_code, 404)
        res = self.app.delete('/users/1/reviews/3')
        self.assertEqual(res.status_code, 404)

    def test_get_my_reviews(self):
        '''User 1 should initially have 0 reviews and then 1.'''
        res = self.app.get('/users/1/my_reviews')
        self.assertEqual(len(json.loads(res.data)), 0)
        self.create_review('/users/2/reviews', 'test', 1)

        res = self.app.get('/users/1/my_reviews')
        self.assertEqual(len(json.loads(res.data)), 1)

    def test_get_place_review(self):
        '''No reviews for this place yet returns empty array. Test a place
        that does not exist, returns 404 status code.'''
        res = self.app.get('/places/1/reviews')
        self.assertEqual(len(json.loads(res.data)), 0)
        res = self.app.get('/places/2/reviews')
        self.assertEqual(res.status_code, 404)

        '''Create a review of place 1 from user 2.'''
        res = self.create_review('/places/1/reviews', 'test', 2)

        res = self.app.get('/places/1/reviews')
        self.assertEqual(len(json.loads(res.data)), 1)

    def test_post_place_review(self):
        '''Test that review is empty and then has one place review after 1
        review is created.'''
        res = self.app.get('/places/1/reviews')
        self.assertEqual(len(json.loads(res.data)), 0)
        self.create_review('/places/1/reviews', 'test', 2)
        res = self.app.get('/places/1/reviews')
        self.assertEqual(len(json.loads(res.data)), 1)

        '''Status code is 404 for an unknown review.'''
        res = self.app.get('/places/2/reviews')
        self.assertEqual(res.status_code, 404)

    def test_post_place_review(self):
        '''A non existant review returns 404 status.'''
        res = self.app.get('/places/1/reviews/1')
        self.assertEqual(res.status_code, 404)

        '''Create a review and test that it is returned using GET request.'''
        self.create_review('/places/1/reviews', 'test', 2)
        res = self.app.get('/places/1/reviews/1')
        self.assertEqual(len(json.loads(res.data)), 1)
        self.assertEqual(json.loads(res.data)[0].get('id'), 1)

    def test_delete_place_review(self):
        '''A non existant review id returns 404 status.'''
        res = self.app.delete('/places/1/reviews/1')
        self.assertEqual(res.status_code, 404)

        '''Create a review and test that it is deleted using DELETE request.'''
        self.create_review('/places/1/reviews', 'test', 2)
        res = self.app.get('/places/1/reviews/1')
        self.assertEqual(len(json.loads(res.data)), 1)

        '''While the review is existant, test if place id does not exist.'''
        res = self.app.delete('/places/2/reviews/1')
        self.assertEqual(res.status_code, 404)

        '''Test that deletion of a review is successfull. A JSON will be
        with a message, so do not test for len of get on this route.'''
        res = self.app.delete('/places/1/reviews/1')
        self.assertEqual(res.status_code, 200)
        res = self.app.get('/places/1/reviews/1')
        self.assertEqual(res.status_code, 404)

        res = self.app.get('/places/1/reviews')
        self.assertEqual(len(json.loads(res.data)), 0)

if __name__ == '__main__':
    unittest.main()
