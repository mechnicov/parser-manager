import configparser
import logging
import os
import unittest

import psycopg2
import requests


URL = "http://127.0.0.1:9292/api/v1/parse"


def connect_db():
    config_path = os.path.join(
        os.path.dirname(__file__), '..', '..', '.env')
    with open(config_path) as f:
        s = '[db_config]\n' + f.read()
    config = configparser.ConfigParser()
    config.read_string(s)

    db_config = config['db_config']

    conn = psycopg2.connect(
        user=db_config['POSTGRES_USER'],
        password=db_config['POSTGRES_PASSWORD'],
        host='0.0.0.0',
        port='5555',
        database=db_config['POSTGRES_DB']
    )

    cur = conn.cursor() 
    return cur


class TestPDF(unittest.TestCase):
    def setUp(self):
        # Load test data
        self.cursor = connect_db()

    def test_valid_file(self):
        data = {
            'url': 'http://test.url/rr',
        }
        files = {
            'file': (
                'rr',
                open(
                    os.path.join(
                        os.path.dirname(__file__), 'fixtures', 'rr'),
                    'rb',
                ),
            )    
        }
        r = requests.post(url=URL, data=data, files=files)
        self.assertEqual(r.status_code, requests.codes.created)
        # Check content written to database
        self.cursor.execute(
            f"SELECT parsed_data, file_type FROM pages WHERE url = '{data['url']}'")
        parsed_data, file_type = self.cursor.fetchone()
        self.assertEqual(parsed_data, 'body\n  \n    ddd\n    \n      paragraph kursiv')
        self.assertEqual(file_type, 'html')
    
    def test_valid_file_with_invalid_ext(self):
        data = {
            'url': 'http://test.url/rr.doc',  # This file have a .pdf type
        }
        files = {
            'file': (
                'invalid.pdf',
                open(
                    os.path.join(
                        os.path.dirname(__file__), 'fixtures', 'rr.doc'),
                    'rb',
                ),
            )    
        }
        r = requests.post(url=URL, data=data, files=files)
        self.assertEqual(r.status_code, requests.codes.created)
        # Check content written to database
        self.cursor.execute(
            f"SELECT parsed_data, file_type FROM pages WHERE url = '{data['url']}'")
        parsed_data, file_type = self.cursor.fetchone()
        self.assertEqual(parsed_data, 'body\n  \n    ddd\n    \n      paragraph kursiv')
        self.assertEqual(file_type, 'html')
    
    def test_no_url(self):
        data = {
        }
        files = {
            'file': (
                'rr',
                open(
                    os.path.join(
                        os.path.dirname(__file__), 'fixtures', 'rr'),
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
                'rr',
                open(
                    os.path.join(
                        os.path.dirname(__file__), 'fixtures', 'rr'),
                    'rb',
                ),
            )    
        }
        r = requests.post(url=URL, data=data, files=files)
        self.assertEqual(r.status_code, requests.codes.unprocessable_entity)
    
    def test_invaild_url(self):
        data = {
            'url': 'test.url/rr',
        }
        files = {
            'file': (
                'rr',
                open(
                    os.path.join(
                        os.path.dirname(__file__), 'fixtures', 'rr'),
                    'rb',
                ),
            )    
        }
        r = requests.post(url=URL, data=data, files=files)
        self.assertEqual(r.status_code, requests.codes.unprocessable_entity)
    
    def test_no_file(self):
        data = {
            'url': 'http://test.url/rr',
        }
        files = { 
        }
        r = requests.post(url=URL, data=data, files=files)
        self.assertEqual(r.status_code, requests.codes.bad_request)
    
    def test_unsopported_file(self):
        data = {
            'url': 'http://test.url/img.jpg',
        }
        files = {
            'file': (
                'img.jpg',
                open(
                    os.path.join(
                        os.path.dirname(__file__), 'fixtures', 'img.jpg'),
                    'rb',
                ),
            )    
        }
        r = requests.post(url=URL, data=data, files=files)
        self.assertEqual(r.status_code, requests.codes.unprocessable_entity)


if __name__ == '__main__':
    unittest.main()