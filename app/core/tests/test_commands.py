"""
Test custom Django management commands.
"""
from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase

# .check method is provided by the Basecommand, which we then inherit to
#  Command


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """test commands"""

    def test_wait_for_db_ready(self, patched_check):
        """test waiting for database if database ready."""
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    # The patched arguments get added into arguments in the order from inside
    # to out So first patched_sleep (time.sleep...) and then patchd_check
    # (core.management.commands...)
    # Time.sleep will replace the built-in sleep function with a magic mock
    # object. We are overriding the behavior of sleep so that we don't actually
    # sleep during test.
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting operational error"""
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.asser_called_with(databases=['default'])
