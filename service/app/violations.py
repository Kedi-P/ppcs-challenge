"""Violation recording — the local state behind ``GET /violations``.

Deliberately small: a non-compliant ``/validate`` result is recorded as a
:class:`Violation` in an in-process repository, and ``/violations`` reads the
recent ones back newest-first. The repository is an interface so the app can be
tested without live Lakebase credentials (see :class:`InMemoryViolationRepository`)
and later backed by a real store without changing the endpoint.

Data minimisation: a violation carries only the fields the contract exposes
(sku, failed rule ids, a redacted human reason, and a timestamp). Prices and
other request payload fields are never stored here.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Protocol


@dataclass(frozen=True)
class Violation:
    """One recorded non-compliant validation."""

    sku: str
    rule_ids: list[str]
    reason: str
    timestamp: datetime


class ViolationRepository(Protocol):
    """Minimal persistence seam for violations.

    Kept intentionally narrow — ``record`` a violation and read the ``recent``
    ones — so an in-memory implementation covers local/CI tests and a future
    Lakebase-backed one can drop in without touching the endpoint.
    """

    def record(self, violation: Violation) -> None: ...

    def recent(self, limit: int) -> list[Violation]: ...


@dataclass
class InMemoryViolationRepository:
    """Process-local violation store, newest-first on read.

    No external dependencies, so ``/violations`` is fully exercisable without
    live Lakebase credentials.
    """

    _items: list[Violation] = field(default_factory=list)

    def record(self, violation: Violation) -> None:
        self._items.append(violation)

    def recent(self, limit: int) -> list[Violation]:
        """Return up to ``limit`` violations, newest verdict first.

        Insertion order breaks timestamp ties (later-recorded wins), so two
        violations stamped in the same instant still read newest-first.
        """
        ordered = sorted(
            enumerate(self._items), key=lambda pair: (pair[1].timestamp, pair[0]), reverse=True
        )
        return [violation for _, violation in ordered][:limit]

    def clear(self) -> None:
        """Drop all recorded violations (test/reset helper)."""
        self._items.clear()
