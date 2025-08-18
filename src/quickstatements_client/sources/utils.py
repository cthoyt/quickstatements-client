"""Utilities for Wikidata."""

from __future__ import annotations

from wikidata_client import get_entity_by_property as get_qid
from wikidata_client import get_image
from wikidata_client import query as query_wikidata

__all__ = [
    "get_image",
    "get_qid",
    "query_wikidata",
]
