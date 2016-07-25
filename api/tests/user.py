from flask_json import JsonTestResponse
from app import app
import unittest
from app.models.base import database
from app.models.user import User

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.app.response_class = JsonTestResponse
        self.client = self.app.test_client()
        database.create_table(User)

    def tearDown(self):
        dat