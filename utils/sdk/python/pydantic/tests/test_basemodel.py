from __future__ import annotations

import logging
from datetime import datetime

import pytest
from pydantic import BaseModel, Field, PositiveInt, ValidationError

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class User(BaseModel):
    id: int
    signup_ts: datetime | None
    tastes: dict[str, PositiveInt]
    name: str = "John Doe"
    height: int | None = Field(None, title="The height in cm", ge=50, le=300)

@pytest.mark.parametrize("data", [
    {"id": 123, "signup_ts": "2019-06-01 12:22", "tastes": {"wine": 9, b"cheese": 7, "cabbage": "1"}},
])
def test_pass(data):
    user = User(**data)
    logger.debug(user.model_dump())

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
