import logging
from datetime import datetime

import pytest
from pydantic import TypeAdapter
from typing_extensions import NotRequired, TypedDict

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Meeting(TypedDict):
    when: datetime
    where: bytes
    why: NotRequired[str]


@pytest.mark.parametrize("data", [
    {"when": "2020-01-01T12:00", "where": "home"},
])
def test_validate(data):
    meeting_adapter = TypeAdapter(Meeting)
    m = meeting_adapter.validate_python(data)
    logger.debug(m)
    meeting_adapter.dump_python(m, exclude={"where"})

def test_json_schema():
    meeting_adapter = TypeAdapter(Meeting)
    logger.debug(meeting_adapter.json_schema())
