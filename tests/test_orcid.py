"""Tests for ORCID."""

import unittest
from typing import cast

from quickstatements_client import CreateLine, EntityLine, TextLine
from quickstatements_client.sources.orcid import check_orcid_exists, iter_orcid_lines


class TestORCID(unittest.TestCase):
    """Tests for ORCID."""

    def test_not_exists(self) -> None:
        """Test checking the API for ORCID records."""
        self.assertFalse(check_orcid_exists("0000-0002-6443-9377"))

    def test_in_wikidata(self) -> None:
        """Test what happens on a page that exists."""
        orcid = "0000-0003-4423-4370"  # Represents Charlie, who already has a page

        lines = list(iter_orcid_lines(orcid, append=False))
        self.assertEqual([], lines)

        lines = list(iter_orcid_lines(orcid, append=True))
        self.assertEqual(3, len(lines))
        instance_line = cast(EntityLine, lines[0])
        occupation_line = cast(EntityLine, lines[1])
        orcid_line = cast(TextLine, lines[2])

        self.assertIsInstance(instance_line, EntityLine)
        self.assertEqual("P31", instance_line.predicate)
        self.assertEqual("Q5", instance_line.target)
        self.assertIsInstance(occupation_line, EntityLine)
        self.assertEqual("P106", occupation_line.predicate)
        self.assertEqual("Q1650915", occupation_line.target)
        self.assertIsInstance(orcid_line, TextLine)
        self.assertEqual(orcid, orcid_line.target)

    def test_not_in_wikidata(self) -> None:
        """Test an ORCID that does not exist in Wikidata."""
        orcid = "0000-0003-4518-7959"  # person from discipline who probably won't get added
        lines = cast(
            tuple[CreateLine, TextLine, TextLine, EntityLine, EntityLine, TextLine],
            tuple(iter_orcid_lines(orcid)),
        )
        self.assertEqual(6, len(lines))
        create_line, len_line, den_line, instance_line, occupation_line, orcid_line = lines

        self.assertIsInstance(create_line, CreateLine)
        self.assertIsInstance(len_line, TextLine)
        self.assertEqual("Len", len_line.predicate)
        self.assertEqual("CHEN chen", len_line.target)
        self.assertIsInstance(den_line, TextLine)
        self.assertEqual("Den", den_line.predicate)
        self.assertIsInstance(instance_line, EntityLine)
        self.assertEqual("P31", instance_line.predicate)
        self.assertEqual("Q5", instance_line.target)
        self.assertIsInstance(occupation_line, EntityLine)
        self.assertEqual("P106", occupation_line.predicate)
        self.assertEqual("Q1650915", occupation_line.target)
        self.assertIsInstance(orcid_line, TextLine)
        self.assertEqual(orcid, orcid_line.target)
