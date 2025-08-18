"""Constants for QuickStatements Client."""

from __future__ import annotations

from typing import TypeAlias

__all__ = [
    "TimeoutHint",
]

#: A type hint for the timeout in :func:`requests.get`
TimeoutHint: TypeAlias = None | int | float | tuple[float | int, float | int]
