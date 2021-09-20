"""
- сгенерировать данные;
- положить их в базу данных;
- отправить REST-запросы;
- сверить результаты с ожидаемыми;
- сгенерировать отчет по результатам.

"""

import logging
import os
import psycopg2
import requests
import unittest
from requests.api import request
import yaml


URL = "http://127.0.0.1:9292/api/v1/parse"


def connect_db():
    config_path = os.path.join(
        os.path.dirname(__file__), '..', '..', 'config', 'database.yml')
    with open(config_path) as f:
        db_config = yaml.safe_load(f)

    try: 
        conn = psycopg2.connect(
            user=db_config['user'],
            # пароль, который указали при установке PostgreSQL
            password=db_config['password'],
            host="127.0.0.1",
            port="5432",
            database=db_config['database']
        )
    except: 
        logging.error("Unable to connect to the database.") 
        return None

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
    
    def test_no_url(self):
        data = {
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
        self.assertEqual(r.status_code, requests.codes.bad_request)
    
    def test_empty_url(self):
        data = {
            'url': '',
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
        self.assertEqual(r.status_code, requests.codes.unprocessable_entity)
    
    def test_invaild_url(self):
        data = {
            'url': 'test.url/docx.docx',
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
        self.assertEqual(r.status_code, requests.codes.unprocessable_entity)
    
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