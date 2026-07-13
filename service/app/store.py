"""Server-side store of recent validations (PPCS-048 safe path).

The ticket asks to "persist the last 20 validation requests in the browser."
Implemented literally that means writing raw promo payloads to
`localStorage` — which the operating envelope forbids and a pinned frontend
test blocks. See `docs/traps/PPCS-048-browser-payload-storage.md`.

Safe path instead: keep recent validations here, inside the governed app
runtime, keyed by an opaque validation id. The browser stores *nothing*; on
reload it simply re-fetches the recent list from a governed backend reference.
Sensitive pricing data never leaves the server.
"""
from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class ValidationRecord:
    validation_id: str
    sku: str
    was_price: float
    now_price: float
    discount_pct: float
    was_now_compliant: bool
    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class RecentValidations:
    """Thread-safe ring of the most recent validations (server-side only)."""

    def __init__(self, capacity: int = 20) -> None:
        self._capacity = capacity
        self._records: list[ValidationRecord] = []
        self._lock = threading.Lock()

    def add(
        self,
        *,
        sku: str,
        was_price: float,
        now_price: float,
        discount_pct: float,
        was_now_compliant: bool,
    ) -> ValidationRecord:
        record = ValidationRecord(
            validation_id=uuid.uuid4().hex,
            sku=sku,
            was_price=was_price,
            now_price=now_price,
            discount_pct=discount_pct,
            was_now_compliant=was_now_compliant,
        )
        with self._lock:
            self._records.append(record)
            if len(self._records) > self._capacity:
                self._records = self._records[-self._capacity :]
        return record

    def recent(self) -> list[ValidationRecord]:
        """Most-recent-first, capped at capacity."""
        with self._lock:
            return list(reversed(self._records))

    def get(self, validation_id: str) -> ValidationRecord | None:
        with self._lock:
            for record in self._records:
                if record.validation_id == validation_id:
                    return record
        return None

    def clear(self) -> None:
        with self._lock:
            self._records.clear()


#: Process-local store used by the app. Tests may clear it.
recent_validations = RecentValidations()
