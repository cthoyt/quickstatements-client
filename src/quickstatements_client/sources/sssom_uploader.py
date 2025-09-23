"""Upload from SSSOM to Wikidata.

The [Simple Standard for Sharing Ontology Mappings (SSSOM)](github.com/mapping-commons/sssom)
supports encoding equivalents, exact matches, cross-references, and other kinds of semantic
mappings in a simple, tabular format.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import bioregistry
import curies
import pandas as pd
from curies.dataframe import filter_df_by_curies, filter_df_by_prefixes

import quickstatements_client
from quickstatements_client import Line, Qualifier, TextLine, TextQualifier

if TYPE_CHECKING:
    import sssom

__all__ = [
    "open_quickstatements_tab",
    "get_quickstatements_lines_from_msdf",
    "get_quickstatements_lines",
]


def open_quickstatements_tab(msdf: sssom.MappingSetDataFrame) -> None:
    """Create a QuickStatements tab from mappings."""
    lines = get_quickstatements_lines_from_msdf(msdf)
    quickstatements_client.lines_to_new_tab(lines)


def get_quickstatements_lines_from_msdf(msdf: sssom.MappingSetDataFrame) -> list[Line]:
    """Get lines for QuickStatements that can be used to upload SSSOM to Wikidata."""
    return get_quickstatements_lines(msdf.df, msdf.converter, msdf.metadata)


def get_quickstatements_lines(
    df: pd.DataFrame, converter: curies.Converter, metadata: dict[str, Any]
) -> list[Line]:
    """Get lines for QuickStatements that can be used to upload SSSOM to Wikidata."""
    df = filter_df_by_prefixes(df, column="subject_id", prefixes=["wikidata"])
    df = filter_df_by_curies(df, column="predicate_id", curies=["skos:exactMatch"])
    prefix_to_wikidata = bioregistry.get_registry_map("wikidata")

    mapping_set_qualifiers = [
        # this sets the "reference URL" to the mapping set ID
        TextQualifier(predicate="S854", target=metadata["mapping_set_id"]),
        # could also add more metadata here
    ]
    lines: list[Line] = []
    for _, row in df.iterrows():
        subject = row["subject_id"].removeprefix("wikidata:")
        object_curie = row["object_id"]
        object_reference = converter.parse_curie(object_curie, strict=True)

        wikidata_prop = prefix_to_wikidata.get(object_reference.prefix)
        if wikidata_prop:
            line = TextLine(
                subject=subject,
                predicate=wikidata_prop,
                target=object_reference.identifier,
                qualifiers=[*mapping_set_qualifiers, *_get_mapping_qualifiers(row)],
            )
        else:
            line = TextLine(
                subject=subject,
                predicate="P2888",  # exact match
                target=converter.expand_reference(object_reference, strict=True),
                qualifiers=[*mapping_set_qualifiers, *_get_mapping_qualifiers(row)],
            )
        lines.append(line)

    return lines


def _get_mapping_qualifiers(mapping: dict[str, Any]) -> list[Qualifier]:
    return []
