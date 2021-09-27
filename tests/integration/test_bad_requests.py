import os
import re
import unittest

import requests


URL = "http://127.0.0.1:9292/api/v1/parse"


class TestBadRequests(unittest.TestCase):
    
    def test_no_url(self):
        filepath = os.path.join(
            os.path.dirname(__file__), 'fixtures', 'pdf.pdf')
        with open(filepath, 'rb') as f:
            data = {
            }
            files = {
                'file': ('pdf.pdf', f)    
            }
            r = requests.post(url=URL, data=data, files=files)
            self.assertEqual(r.status_code, requests.codes.bad_request)
    
    def test_empty_url(self):
        filepath = os.path.join(
            os.path.dirname(__file__), 'fixtures', 'pdf.pdf')
        with open(filepath, 'rb') as f:
            data = {
                'url': '',
            }
            files = {
                'file': ('pdf.pdf', f)    
            }
            r = requests.post(url=URL, data=data, files=files)
            self.assertEqual(r.status_code, requests.codes.unprocessable_entity)
    
    def test_invaild_url(self):
        filepath = os.path.join(
            os.path.dirname(__file__), 'fixtures', 'pdf.pdf')
        with open(filepath, 'rb') as f:
            data = {
                'url': 'test.url/pdf.pdf',
            }
            files = {
                'file': ('pdf.pdf', f)    
            }
            r = requests.post(url=URL, data=data, files=files)
            self.assertEqual(r.status_code, requests.codes.unprocessable_entity)
    
    def test_unsopported_file(self):
        filepath = os.path.join(
            os.path.dirname(__file__), 'fixtures', 'img.jpg')
        with open(filepath, 'rb') as f:
            data = {
                'url': 'http://test.url/img.jpg',
            }
            files = {
                'file': ('img.jpg', f)    
            }
            r = requests.post(url=URL, data=data, files=files)
            self.assertEqual(r.status_code, requests.codes.unprocessable_entity)


if __name__ == '__main__':
    unittest.main()