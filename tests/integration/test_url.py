import os
import re
import unittest

import requests


URL = "http://127.0.0.1:9292/api/v1/parse"


class TestURL(unittest.TestCase):
    
    def test_no_url(self):
        data = {
        }
        files = {
            'file': (
                'pdf.pdf',
                open(
                    os.path.join(
                        os.path.dirname(__file__), 'fixtures', 'pdf.pdf'),
                    'rb',
                ),
            )    
        }
        r = requests.post(url=URL, data=data, files=files)
        self.assertEqual(r.status_code, requests.codes.bad_request)
    
    def test_empty_url(self):
        data = {
            'url': '',
        }
        files = {
            'file': (
                'pdf.pdf',
                open(
                    os.path.join(
                        os.path.dirname(__file__), 'fixtures', 'pdf.pdf'),
                    'rb',
                ),
            )    
        }
        r = requests.post(url=URL, data=data, files=files)
        self.assertEqual(r.status_code, requests.codes.unprocessable_entity)
    
    def test_invaild_url(self):
        data = {
            'url': 'test.url/pdf.pdf',
        }
        files = {
            'file': (
                'pdf.pdf',
                open(
                    os.path.join(
                        os.path.dirname(__file__), 'fixtures', 'pdf.pdf'),
                    'rb',
                ),
            )    
        }
        r = requests.post(url=URL, data=data, files=files)
        self.assertEqual(r.status_code, requests.codes.unprocessable_entity)


if __name__ == '__main__':
    unittest.main()