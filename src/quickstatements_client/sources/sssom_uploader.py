"""
The [Simple Standard for Sharing Ontology Mappings (SSSOM)](github.com/mapping-commons/sssom)
supports encoding equivalents, exact matches, cross-references, and other kinds of semantic
mappings in a simple, tabular format.
"""

import bioregistry
import quickstatements_client
from curies.dataframe import filter_df_by_curies, filter_df_by_prefixes
from quickstatements_client import Line, Qualifier, TextLine, TextQualifier

import sssom
from sssom import MappingSetDataFrame


def open_quickstatements_tab(msdf: MappingSetDataFrame) -> None:
    """Create a QuickStatements tab from mappings."""
    lines = get_quickstatements_lines(msdf)
    quickstatements_client.lines_to_new_tab(lines)


def get_quickstatements_lines(msdf: MappingSetDataFrame) -> list[Line]:
    """Get lines for QuickStatements that can be used to upload SSSOM to Wikidata."""
    df = filter_df_by_prefixes(msdf.df, column="subject_id", prefixes=["wikidata"])
    df = filter_df_by_curies(df, column="predicate_id", curies=["skos:exactMatch"])
    prefix_to_wikidata = bioregistry.get_registry_map("wikidata")

    mapping_set_qualifiers = [
        TextQualifier(predicate="S854", text=msdf.metadata["mapping_set_id"]),
        # could also add more metadata here
    ]
    lines: list[Line] = []
    for subject_curie, object_curie in df[["subject_id", "object_id"]].values:
        subject = subject_curie.removeprefix("wikidata:")
        o_reference = msdf.converter.parse_curie(object_curie, strict=True)

        wikidata_prop = prefix_to_wikidata.get(o_reference.prefix)
        if wikidata_prop:
            line = TextLine(
                subject=subject,
                predicate=wikidata_prop,
                target=o_reference.identifier,
                qualifiers=[*mapping_set_qualifiers],
            )
        else:
            line = TextLine(
                subject=subject,
                predicate="P2888",  # exact match
                target=msdf.converter.expand(object_curie, strict=True),
                qualifiers=[*mapping_set_qualifiers],
            )
        lines.append(line)

    return lines


def _get_mapping_qualifiers(mapping: sssom.Mapping) -> list[Qualifier]:
    return []
