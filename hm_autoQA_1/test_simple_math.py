import pytest
from simple_math import SimpleMath

@pytest.fixture
def math_obj():
    return SimpleMath()


@pytest.mark.parametrize("input_value, expected", [
    (2, 4),
    (0, 0),
    (-3, 9),
    (5, 25)
])
def test_square(math_obj, input_value, expected):
    assert math_obj.square(input_value) == expected


@pytest.mark.parametrize("input_value, expected", [
    (2, 8),
    (0, 0),
    (-3, -27),
    (4, 64)
])
def test_cube(math_obj, input_value, expected):
    assert math_obj.cube(input_value) == expected
