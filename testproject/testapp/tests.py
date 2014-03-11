import pytest

from . import models


def test_uninitialized_access_raises_error():
    """Accessing a value that doesn't exist raises DoesNotExist."""

    with pytest.raises(models.Race.DoesNotExist):
        models.Race.WHITE
