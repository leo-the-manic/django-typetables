import django.core.management
import django.test

from . import models


class TypetableTest(django.test.TestCase):

    def test_uninitialized_access_raises_error(self):
        """Accessing a value that doesn't exist raises DoesNotExist."""

        self.assertRaises(models.Race.DoesNotExist, lambda: models.Race.WHITE)

    def test_install_command_installs(self):
        """The 'typetable_install' command installs typetable values."""
        django.core.management.call_command('typetable_install')

        expected_names = [
            'Black/African American', 'White', 'American Indian/Alaska Native',
            'Asian/Pacific Islander', 'Hispanic/Latin American']
        self.assertEqual(len(expected_names), models.Race.objects.count())
        for name in expected_names:
            self.assertTrue(models.Race.objects.filter(name=name).exists())
