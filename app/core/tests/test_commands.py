# Test custom Django management commands.
from unittest.mock import patch
from psycopg2 import OperationalError as Psycopg2Error  # type: ignore
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    # Test commands
    def test_wait_for_db_ready(self, patched_check):
        # Test that the database is ready
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        # Test waiting for database when getting OperationalError.
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        '''
        The first two times we call this, raise the psycopg2 error,
        then the next 3 times, call the operational error.
        Finally, return true. This should test a wide range of cases.
        '''
        call_command('wait_for_db')

        # We're testing to see if the patched_check was called 6 times
        self.assertEqual(patched_check.call_count, 6)

        # Make sure that patched_check is called with the correct values
        patched_check.assert_called_with(databases=['default'])
