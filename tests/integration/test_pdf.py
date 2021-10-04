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


class TestPDF(unittest.TestCase):
    def setUp(self):
        # Load test data
        self.cursor = connect_db()

    def test_valid_file(self):
        filepath = os.path.join(
            os.path.dirname(__file__), 'fixtures', 'pdf.pdf')
        with open(filepath, 'rb') as f:
            data = {
                'url': 'http://test.url/pdf.pdf',
            }
            files = {
                'file': ('pdf.pdf', f)
            }
            r = requests.post(url=URL, data=data, files=files)
            self.assertEqual(r.status_code, requests.codes.created)
            # Check content written to database
            self.cursor.execute(
                f"SELECT parsed_data, file_type FROM pages WHERE url = '{data['url']}'")
            parsed_data, file_type = self.cursor.fetchone()
            self.assertIsNotNone(
                re.fullmatch(
                    r'Привет, как *дела\n+Всё хорошо!\n+ *Супер', parsed_data
                )
            )
            self.assertEqual(file_type, 'pdf')
    
    def test_valid_file_with_invalid_ext(self):
        filepath = os.path.join(
            os.path.dirname(__file__), 'fixtures', 'pdf.docx')
        with open(filepath, 'rb') as f:
            data = {
                'url': 'http://test.url/pdf.docx',  # This file have a .pdf type
            }
            files = {
                'file': ('invalid.pdf', f)    
            }
            r = requests.post(url=URL, data=data, files=files)
            self.assertEqual(r.status_code, requests.codes.created)
            # Check content written to database
            self.cursor.execute(
                f"SELECT parsed_data, file_type FROM pages WHERE url = '{data['url']}'")
            parsed_data, file_type = self.cursor.fetchone()
            self.assertIsNotNone(
                re.fullmatch(
                    r'Привет, как *дела\n+Всё хорошо!\n+ *Супер', parsed_data
                )
            )
            self.assertEqual(file_type, 'pdf')

    def test_rotated_file(self):
        filepath = os.path.join(
            os.path.dirname(__file__), 'fixtures', 'rotate.pdf')
        with open(filepath, 'rb') as f:
            data = {
                'url': 'http://test.url/rotate.pdf',
            }
            files = {
                'file': ('rotate.pdf', f)
            }
            r = requests.post(url=URL, data=data, files=files)
            self.assertEqual(r.status_code, requests.codes.created)
            # Check content written to database
            self.cursor.execute(
                f"SELECT parsed_data, file_type FROM pages WHERE url = '{data['url']}'")
            parsed_data, file_type = self.cursor.fetchone()
            self.assertIsNotNone(
                re.fullmatch(
                    r'Привет, как *дела\n+Всё хорошо!\n+ *Супер', parsed_data
                )
            )
            self.assertEqual(file_type, 'pdf')

    def test_symbols(self):
        filepath = os.path.join(
            os.path.dirname(__file__), 'fixtures', 'symbols.pdf')
        check_filepath = os.path.join(
            os.path.dirname(__file__), 'fixtures', 'symbols.txt')
        with open(filepath, 'rb') as f:
            data = {
                'url': 'http://test.url/symbols.pdf',
            }
            files = {
                'file': ('symbols.pdf', f)
            }
            r = requests.post(url=URL, data=data, files=files)
            self.assertEqual(r.status_code, requests.codes.created)
            # Check content written to database
            self.cursor.execute(
                f"SELECT parsed_data, file_type FROM pages WHERE url = '{data['url']}'")
            parsed_data, file_type = self.cursor.fetchone()
            with open(check_filepath, 'r') as cf:
                self.assertEqual(unificate(parsed_data), unificate(cf.read()))
            self.assertEqual(file_type, 'pdf')

    def test_empty_file(self):
        filepath = os.path.join(
            os.path.dirname(__file__), 'fixtures', 'empty.pdf')
        with open(filepath, 'rb') as f:
            data = {
                'url': 'http://test.url/empty.pdf',
            }
            files = {
                'file': ('empty.pdf', f)    
            }
            r = requests.post(url=URL, data=data, files=files)
            self.assertEqual(r.status_code, requests.codes.unprocessable_entity)

    def test_big_file(self):
        filepath = os.path.join(
            os.path.dirname(__file__), 'fixtures', 'big.pdf')
        with open(filepath, 'rb') as f:
            data = {
                'url': 'http://test.url/big.pdf',
            }
            files = {
                'file': ('pdf.pdf', f)    
            }
            r = requests.post(url=URL, data=data, files=files)
            self.assertEqual(r.status_code, requests.codes.created)


if __name__ == '__main__':
    unittest.main()