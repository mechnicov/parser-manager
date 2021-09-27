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
            'url': 'http://test.url/docx.docx',
        }
        files = {
            'file': (
                'docx.docx',
                open(
                    os.path.join(
                        os.path.dirname(__file__), 'fixtures', 'docx.docx'),
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
        self.assertEqual(parsed_data, 'Привет, как дела\nВсё хорошо!\nСупер')
        self.assertEqual(file_type, 'docx')
    
    def test_valid_file_with_invalid_ext(self):
        data = {
            'url': 'http://test.url/docx.html',  # This file have a .pdf type
        }
        files = {
            'file': (
                'invalid.pdf',
                open(
                    os.path.join(
                        os.path.dirname(__file__), 'fixtures', 'docx.html'),
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
        self.assertEqual(parsed_data, 'Привет, как дела\nВсё хорошо!\nСупер')
        self.assertEqual(file_type, 'docx')
        
    def test_no_file(self):
        data = {
            'url': 'http://test.url/docx.docx',
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