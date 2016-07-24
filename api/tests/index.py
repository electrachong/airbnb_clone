#import os
from flask_json import JsonTestResponse
from app import app
#from config import *
#from app.models.base import database
#from migrate import create_tables 
import unittest
#import tempfile

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.app.response_class = JsonTestResponse
        self.client = self.app.test_client()
        
        # create_tables()

    # def tearDown(self):
    #     database.session.remove()
    #     database.drop_all()

    def test_200(self):
        test_res = self.client.get('/')
        assert test_res.status_code == "200", "Status Code is NOT 200"

    # def tearDown(self):
    #     os.close(self.db_fd)
    #     os.unlink(flaskr.app.config['DATABASE'])

if __name__ == '__main__':
    unittest.main()