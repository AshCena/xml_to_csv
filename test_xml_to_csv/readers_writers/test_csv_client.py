import unittest
from unittest.mock import patch, MagicMock
from sqlalchemy.exc import SQLAlchemyError
# from sqs_fetch.readers_writers.db_client import DBClient


class TestDBClient(unittest.TestCase):

    def setUp(self):
        self.db_path = 'sqlite:///:memory:'
        self.data = [MagicMock()]

    def test_write_data(self):
        return True