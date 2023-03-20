import pytest
from FieldManager.FieldManager import FieldManager
from Point.Point import Point


def test_FieldManager_low_size():
    with pytest.raises(ValueError) as e:
        FieldManager(
            size=-5, start=Point(10.0, 10.0), end=Point(250.0, 250.0), seed=80
        )
    assert str(e.value) == "field size must be greater than 0"


def test_FieldManager_invalid_corrdinate():
    with pytest.raises(ValueError) as e:
        FieldManager(
            size=300, start=Point(-5.0, 10.0), end=Point(250.0, 250.0), seed=80
        )
    assert str(e.value) == "invalid coordinate"
