import configparser
import os
import re
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
        filepath = os.path.join(
            os.path.dirname(__file__), 'fixtures', 'rr')
        with open(filepath, 'rb') as f:
            data = {
                'url': 'http://test.url/rr',
            }
            files = {
                'file': ('rr', f)    
            }
            r = requests.post(url=URL, data=data, files=files)
            self.assertEqual(r.status_code, requests.codes.created)
            # Check content written to database
            self.cursor.execute(
                f"SELECT parsed_data, file_type FROM pages WHERE url = '{data['url']}'")
            parsed_data, file_type = self.cursor.fetchone()
            self.assertIsNotNone(
                re.fullmatch(
                    r'body\n *\n *ddd\n *\n *paragraph kursiv', parsed_data
                )
            )
            self.assertEqual(file_type, 'html')
    
    def test_valid_file_with_invalid_ext(self):
        filepath = os.path.join(
            os.path.dirname(__file__), 'fixtures', 'rr.doc')
        with open(filepath, 'rb') as f:
            data = {
                'url': 'http://test.url/rr.doc',  # This file have a .pdf type
            }
            files = {
                'file': ('invalid.html', f)    
            }
            r = requests.post(url=URL, data=data, files=files)
            self.assertEqual(r.status_code, requests.codes.created)
            # Check content written to database
            self.cursor.execute(
                f"SELECT parsed_data, file_type FROM pages WHERE url = '{data['url']}'")
            parsed_data, file_type = self.cursor.fetchone()
            self.assertIsNotNone(
                re.fullmatch(
                    r'body\n *\n *ddd\n *\n *paragraph kursiv', parsed_data
                )
            )
            self.assertEqual(file_type, 'html')
    
    def test_no_file(self):
        data = {
            'url': 'http://test.url/rr',
        }
        files = {}
        r = requests.post(url=URL, data=data, files=files)
        self.assertEqual(r.status_code, requests.codes.bad_request)


if __name__ == '__main__':
    unittest.main()