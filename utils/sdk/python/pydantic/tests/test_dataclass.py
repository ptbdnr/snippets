from __future__ import annotations

import dataclasses
import logging
from datetime import datetime

import pytest
from pydantic import PositiveInt, ValidationError
from pydantic.dataclasses import dataclass

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@dataclass
class User:
    id: int
    signup_ts: datetime | None
    tastes: dict[str, PositiveInt]
    name: str = "John Doe"
    friends: list[int] = dataclasses.field(default_factory=lambda: [0])
    age: int | None = dataclasses.field(
        default=None,
        metadata={"title": "The age of the user", "description": "do not lie!"},
    )


@pytest.mark.parametrize("data", [
    {"id": 123, "signup_ts": "2019-06-01 12:22", "tastes": {"wine": 9, b"cheese": 7, "cabbage": "1"}},
])
def test_pass(data):
    User(**data)

@pytest.mark.parametrize("data", [
    {"id": "not an int", "tastes": {}},
])
def test_fail(data):
    with pytest.raises(ValidationError):
        try:
            User(**data)
        except ValidationError as err:
            logger.debug(err.errors())
            raise err
