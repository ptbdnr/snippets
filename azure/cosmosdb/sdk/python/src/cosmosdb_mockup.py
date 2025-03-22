from __future__ import annotations

from typing import ClassVar, Optional

from src.cosmosdb_abstract import CosmosDBAbstract


class CosmosDBMockup(CosmosDBAbstract):
    """Mockup class for data store."""

    mockup_items: ClassVar[list[dict]] = [{
        "id": "FOO",
        "key": "FOO",
        "definition": "FOO is BAR and BUZ",
    }]

    def list_databases(self) -> list:
        """List databases."""
        return ["mockup_db"]

    def insert(self, payload: dict) -> dict:
        """Insert a payload."""
        return payload

    def insert_many(self, payloads: list[dict]) -> list:
        """Insert many payloads."""
        return [self.insert(payload) for payload in payloads]

    def find(self, filter: Optional[dict]) -> list:
        """Find items."""
        return self.mockup_items
