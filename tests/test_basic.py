# pylint: disable=C0116
"""
This is a basic test file for demonstrating simple pytest functionality.

Tests:
- `test_add()`: A basic test function that asserts whether 1 + 1 equals 2.
- `test_assert()`: Checks whether a simple condition is True.
  The test passes if `condition` is True.
- `test_raises_ValueError()`: Demonstrates `pytest.raises`
  by asserting a `ValueError`.
- `test_raises_ImportError()`: Demonstrates `pytest.raises`
  by asserting an `ImportError`.
- `test_warn()`: Shows `pytest.warns` functionality,
  which checks for a `UserWarning`.

Each test highlights common pytest functionality:
- Basic assertions (`assert`),
- Error handling with `pytest.raises`, and
- Warning testing with `pytest.warns`.
"""
from warnings import warn
import pytest


def test_add():
    assert 1+1 == 2


def test_assert():
    # Change to pass_test = False to test failure
    pass_test = True
    assert pass_test


def test_raise_valueerror():
    with pytest.raises(ValueError):
        raise ValueError("Testing ValueError")


def test_raise_importerror():
    with pytest.raises(ImportError):
        raise ImportError("Testing ImportError")


def test_warn():
    with pytest.warns(UserWarning):
        warn('Testing warn')
