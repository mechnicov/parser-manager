import configparser
import os
import re
import unittest

import psycopg2
import requests

from create_regular_string import unificate


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


class TestHTML(unittest.TestCase):
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
            self.assertEqual(unificate(parsed_data), unificate('body\n  \n  ddd\n  \n  paragraph kursiv'))
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
            self.assertEqual(unificate(parsed_data), unificate('body\n  \n  ddd\n  \n  paragraph kursiv'))
            self.assertEqual(file_type, 'html')

    def test_valid_file_with_tags(self):
        filepath = os.path.join(
            os.path.dirname(__file__), 'fixtures', 'body.html')
        with open(filepath, 'rb') as f:
            data = {
                'url': 'http://test.url/body.html',
            }
            files = {
                'file': ('body.html', f)    
            }
            r = requests.post(url=URL, data=data, files=files)
            self.assertEqual(r.status_code, requests.codes.created)
            # Check content written to database
            self.cursor.execute(
                f"SELECT parsed_data, file_type FROM pages WHERE url = '{data['url']}'")
            parsed_data, file_type = self.cursor.fetchone()
            self.assertEqual(unificate(parsed_data), unificate('body\n  \n  ddd\n  \n  paragraph kursiv\n  \n  <body>everybody</body>'))
            self.assertEqual(file_type, 'html')

    def test_symbols(self):
        filepath = os.path.join(
            os.path.dirname(__file__), 'fixtures', 'symbols.html')
        check_filepath = os.path.join(
            os.path.dirname(__file__), 'fixtures', 'symbols.txt')
        with open(filepath, 'rb') as f:
            data = {
                'url': 'http://test.url/symbols.html',
            }
            files = {
                'file': ('symbols.html', f)
            }
            r = requests.post(url=URL, data=data, files=files)
            self.assertEqual(r.status_code, requests.codes.created)
            # Check content written to database
            self.cursor.execute(
                f"SELECT parsed_data, file_type FROM pages WHERE url = '{data['url']}'")
            parsed_data, file_type = self.cursor.fetchone()
            with open(check_filepath, 'r') as cf:
                self.assertEqual(unificate(parsed_data), unificate(cf.read()))
            self.assertEqual(file_type, 'html')

    def test_empty_file(self):
        filepath = os.path.join(
            os.path.dirname(__file__), 'fixtures', 'empty.html')
        with open(filepath, 'rb') as f:
            data = {
                'url': 'http://test.url/empty.html',
            }
            files = {
                'file': ('empty.html', f)    
            }
            r = requests.post(url=URL, data=data, files=files)
            self.assertEqual(r.status_code, requests.codes.unprocessable_entity)


if __name__ == '__main__':
    unittest.main()