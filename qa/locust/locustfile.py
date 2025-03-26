import logging
import time
from random import randint
from typing import ClassVar

from locust import FastHttpUser, between, task

API_BASE_URL = 'foo'
API_KEY = 'key'

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)

logger.info("API_BASE_URL: %s", API_BASE_URL)


class QueryLoadTest(FastHttpUser):
    """Load test."""

    weight = 1
    wait_time = between(0.1, 0.1)
    host = API_BASE_URL
    api_headers : ClassVar[dict] = {
        "Accept": "application/vnd.github.v3+json",
        "Ocp-Apim-Subscription-Key": API_KEY,
    }

    def on_start(self) -> None:
        """Start load test."""
        logger.info("Starting load test")
        logger.info("host: %s", self.host)

    @task(1)
    def api_route(self) -> None:
        """Loadtest API /route."""
        with self.client.post(
            url="/api_route",
            headers=self.api_headers,
            json={
                "data": "foo",
            },
            name="/api_route",
        ) as response:
            logger.info("Status code: %s", response.status_code)
            if response.status_code == 200:
                logger.info("Response content: %s", response.content)
        time.sleep(0.1)

    def on_stop(self) -> None:
        """Stop load test."""
        print("Stopping load test")
