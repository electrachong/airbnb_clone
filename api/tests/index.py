from flask_json import JsonTestResponse
from app import app
import unittest
from datetime import datetime

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.app.response_class = JsonTestResponse
        self.client = self.app.test_client()

    def test_200(self):
        test_res = self.client.get('/')
        assert test_res.status_code == "200", "Status Code is NOT 200, or does not exist"

    def test_status(self):
        test_res = self.client.get('/')
        assert test_res.json['status'] == "OK", "Status is NOT OK, or does not exist"

    def test_time(self):
        test_res = self.client.get('/')
        now = datetime.now().strftime("%Y/%m/%d %H:%M")
        try:
            day = datetime.strptime(test_res.json['time'], "%Y/%m/%d %H:%M:%S")
        except ValueError as e:
            raise AssertionError("'time' in response body is not formatted properly (Y/m/d H:M:S)")
        assert now == day.strftime("%Y/%m/%d %H:%M"), "Time is not current"
    
    def test_time_utc(self):
        test_res = self.client.get('/')
        now = datetime.now().strftime("%Y/%m/%d %H:%M")
        try:
            day = datetime.strptime(test_res.json['time'], "%Y/%m/%d %H:%M:%S")
        except ValueError as e:
            raise AssertionError("'utc_time' in response body is not formatted properly (Y/m/d H:M:S)")
        assert now == day.strftime("%Y/%m/%d %H:%M"), "Time is not current"
    

if __name__ == '__main__':
    unittest.main()