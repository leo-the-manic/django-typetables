import django.core.management
import pytest

from . import models


def test_uninitialized_access_raises_error():
    """Accessing a value that doesn't exist raises DoesNotExist."""

    with pytest.raises(models.Race.DoesNotExist):
        models.Race.WHITE


def test_install_command_installs():
    """The 'typetable_install' command installs typetable values."""
    django.core.management.call_command('typetable_install')

    expected_names = [
        'Black/African American', 'White', 'American Indian/Alaska Native',
        'Asian/Pacific Islander', 'Hispanic/Latin American']
    assert models.Race.objects.count() == len(expected_names)
    for name in expected_names:
        assert models.Race.objects.filter(name=name).exists()
