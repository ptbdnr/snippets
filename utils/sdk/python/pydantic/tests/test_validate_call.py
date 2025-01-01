import logging
from datetime import date
from typing import Annotated

import pytest
from pydantic import Field, ValidationError, validate_call

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@validate_call
def repeat(s: str, count: int, *, separator: bytes = b"") -> bytes:
    b = s.encode()
    return separator.join(b for _ in range(count))


@pytest.mark.parametrize("data", [
    ("hello", 3),
])
def test_pass(data):
    a = repeat(*data)
    logger.debug(a)


@pytest.mark.parametrize(("data", "kwdata"), [
    (("x", 4), {"separator": b" "}),
])
def test_pass_kwargs(data, kwdata):
    a = repeat(*data, **kwdata)
    logger.debug(a)


@pytest.mark.parametrize(("data", "kwdata"), [
    (("good bye", 2), {"separator": b", "}),
])
def test_pass_kwargs_original_function(data, kwdata):
    b = repeat.raw_function(*data, **kwdata)
    logger.debug(b)



@pytest.mark.parametrize("data", [
    ("hello", "wrong"),
])
def test_fail(data):
    with pytest.raises(ValidationError):
        try:
            c = repeat(*data)
        except ValidationError as err:
            logger.debug(err.errors())
            raise err


@validate_call
def greater_than(d1: date, d2: date, *, include_equal=False) -> date:
    if include_equal:
        return d1 >= d2
    return d1 > d2


@pytest.mark.parametrize("data", [
    ("2000-01-01", date(2001, 1, 1)),
])
def test_pass_parameters_types(data):
    greater_than(*data, include_equal=True)


@validate_call
def how_many(num: Annotated[int, Field(gt=10, alias='number')]):
    return num


@pytest.mark.parametrize("value", [
    42,
])
def test_pass_alias(value):
    how_many(value)


@pytest.mark.parametrize("value", [
    1,
])
def test_fail_using_field(value):
    with pytest.raises(ValidationError):
        try:
            how_many(value)
        except ValidationError as err:
            logger.debug(err.errors())
            raise err
