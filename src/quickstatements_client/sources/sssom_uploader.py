"""Upload from SSSOM to Wikidata.

The [Simple Standard for Sharing Ontology Mappings (SSSOM)](github.com/mapping-commons/sssom)
supports encoding equivalents, exact matches, cross-references, and other kinds of semantic
mappings in a simple, tabular format.
"""

from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING, Any

import bioregistry
import curies
import pandas as pd
import wikidata_client
from curies.dataframe import filter_df_by_curies, filter_df_by_prefixes, get_df_unique_prefixes

import quickstatements_client
from quickstatements_client import Line, Qualifier, TextLine, TextQualifier

if TYPE_CHECKING:
    import sssom

__all__ = [
    "get_quickstatements_lines",
    "get_quickstatements_lines_from_msdf",
    "open_quickstatements_tab",
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

    # TODO use curies.Converter operation for this?
    df["wikidata_id"] = df["subject_id"].str.removeprefix("wikidata:")

    mapping_set_qualifiers = [
        # this sets the "reference URL" to the mapping set ID
        TextQualifier(predicate="S854", target=metadata["mapping_set_id"]),
        # could also add more metadata here
    ]

    prefix_to_wikidata = bioregistry.get_registry_map("wikidata")

    wikidata_ids = df["wikidata_id"].unique().tolist()

    wikidata_id_to_references = _get_wikidata_to_property_matches(
        wikidata_ids, df, converter, prefix_to_wikidata
    )
    wikidata_id_to_exact = _get_wikidata_to_exact_matches(wikidata_ids)

    lines: list[Line] = []
    for _, row in df.iterrows():
        subject = row["wikidata_id"]
        object_curie = row["object_id"]
        object_reference = converter.parse_curie(object_curie, strict=True)

        wikidata_prop = prefix_to_wikidata.get(object_reference.prefix)
        if wikidata_prop:
            if object_reference not in wikidata_id_to_references.get(subject, set()):
                line = TextLine(
                    subject=subject,
                    predicate=wikidata_prop,
                    target=object_reference.identifier,
                    qualifiers=[*mapping_set_qualifiers, *_get_mapping_qualifiers(row)],
                )
        else:
            object_uri = converter.expand_reference(object_reference, strict=True)
            if object_uri not in wikidata_id_to_exact.get(subject, set()):
                line = TextLine(
                    subject=subject,
                    predicate="P2888",  # exact match
                    target=object_uri,
                    qualifiers=[*mapping_set_qualifiers, *_get_mapping_qualifiers(row)],
                )
        lines.append(line)

    return lines


def _get_wikidata_to_property_matches(
    wikidata_ids: list[str],
    df: pd.DataFrame,
    converter: curies.Converter,
    prefix_to_wikidata: dict[str, str] | None = None,
) -> dict[str, set[curies.Reference]]:
    if prefix_to_wikidata is None:
        prefix_to_wikidata = bioregistry.get_registry_map("wikidata")

    rv: defaultdict[str, set[curies.Reference]] = defaultdict(set)
    for prefix in get_df_unique_prefixes(
        df, column="object_id", converter=converter, validate=True
    ):
        if wdp := prefix_to_wikidata.get(prefix):
            property_reference_sparql = f"""\
                SELECT ?s ?o WHERE {{
                    VALUES ?s {{ {" ".join(wikidata_ids)} }}
                    ?s wdt:{wdp} ?o .
                }}
            """
            for subject_id, object_id in wikidata_client.query(property_reference_sparql):
                # FIXME handle what comes out of query
                rv[subject_id].add(curies.Reference(prefix=prefix, identifier=object_id))

    return dict(rv)


def _get_wikidata_to_exact_matches(wikidata_ids: list[str]) -> dict[str, set[str]]:
    sparql2 = f"""\
        SELECT ?s ?p ?o WHERE {{
            VALUES ?s {{ {" ".join(wikidata_ids)} }}
            ?s wdt:P2888 ?o .
        }}
    """
    rv: defaultdict[str, set[str]] = defaultdict(set)
    for subject, object_uri in wikidata_client.query(sparql2):
        # FIXME handle what comes out of query
        rv[subject].add(object_uri)
    return dict(rv)


def _get_mapping_qualifiers(mapping: dict[str, Any]) -> list[Qualifier]:
    return []
