import pytest
from FieldManager.FieldManager import FieldManager


def test_field1():
    with pytest.raises(ValueError) as e:
        FieldManager(size=-5, start=(10.0, 10.0), end=(250.0, 250.0), seed=80)
    assert str(e.value) == 'field size must be greater than 0'


def test_field2():
    with pytest.raises(ValueError) as e:
        FieldManager(size=300, start=(-5.0, 10.0), end=(250.0, 250.0), seed=80)
    assert str(e.value) == 'invalid coordinate'
