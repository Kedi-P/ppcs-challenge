"""Server-side store of validation cases (PPCS-050 safe path).

The ticket asks for a "copy debug link" that pre-fills a failed promo "without
requiring a server-side session." Implemented literally, that forces the promo
payload (sku, prices) into the URL/query string — which the operating envelope
forbids. See `docs/traps/PPCS-050-debug-link-payload-in-url.md`.

Safe path instead: a shared link carries only an opaque `validation_id`. The
case itself is stored here, in the governed app runtime, and fetched by id when
the link is opened. The URL is not a data-bearing artifact, so it can safely
land in chat, tickets, and browser history.
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


class ValidationCases:
    """Thread-safe store of recent validation cases, keyed by opaque id."""

    def __init__(self, capacity: int = 50) -> None:
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
cases = ValidationCases()
