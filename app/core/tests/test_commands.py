from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):

    def test_wait_for_db_ready(self):
        """
        Test to check if DB is ready when it is available.
        """
        with patch('django.db.utils.ConnectionHandler.__getitem__') as db_handler:
            db_handler.return_value = True
            call_command('wait_for_db')
            self.assertEqual(db_handler.call_count, 1)

    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """
        Test to check if DB is available.

        When checking for DB, we wait a second after each DB availability call in case it is not available
        and on the 6th try it returns True which means its available. For unavailability, we raise
        OperationalError. Finally we assert that the total number of calls to that ConnectionHandler were 6.
        5 failures and 1 success.
        """
        with patch('django.db.utils.ConnectionHandler.__getitem__') as db_handler:
            db_handler.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(db_handler.call_count, 6)
