"""Deduplication tests using synthetic fixtures only."""

from __future__ import annotations

import json
import unittest

import helpers  # noqa: F401

from hoaxscope_ml.data.dedup import (
    DedupConfig,
    build_dedup_result,
    find_near_duplicate_pairs,
    url_groups,
)


class DedupTests(unittest.TestCase):
    def test_url_grouping(self) -> None:
        records = [
            helpers.make_record(1, "alpha one two three", url_group_id="url-a"),
            helpers.make_record(2, "zulu nine eight seven", url_group_id="url-a"),
            helpers.make_record(3, "kappa five four six", url_group_id="url-b"),
        ]
        groups = url_groups(records)
        self.assertEqual(len(groups), 2)
        self.assertEqual(len(groups["url-a"]), 2)

        result = build_dedup_result(records, DedupConfig(shingle_size=3))
        self.assertEqual(result.records[0].duplicate_group_id, result.records[1].duplicate_group_id)
        self.assertNotEqual(result.records[0].duplicate_group_id, result.records[2].duplicate_group_id)

    def test_near_duplicate_grouping(self) -> None:
        records = [
            helpers.make_record(1, "alpha beta gamma delta epsilon"),
            helpers.make_record(2, "alpha beta gamma delta epsilon zeta"),
            helpers.make_record(3, "omega sigma rho tau upsilon"),
        ]
        pairs = find_near_duplicate_pairs(records, DedupConfig(shingle_size=3))
        self.assertEqual(pairs, [(0, 1)])

    def test_transitive_connected_components(self) -> None:
        records = [
            helpers.make_record(1, "a b c d e"),
            helpers.make_record(2, "a b c d e f"),
            helpers.make_record(3, "b c d e f g"),
        ]
        config = DedupConfig(shingle_size=3, similarity_threshold=0.5)
        pairs = find_near_duplicate_pairs(records, config)
        self.assertIn((0, 1), pairs)
        self.assertIn((1, 2), pairs)
        self.assertNotIn((0, 2), pairs)

        result = build_dedup_result(records, config)
        self.assertEqual(len({record.duplicate_group_id for record in result.records}), 1)

    def test_label_conflict_detection_and_quarantine(self) -> None:
        records = [
            helpers.make_record(
                1, "synthetic repeated article text", source_label="Valid"
            ),
            helpers.make_record(
                2, "synthetic repeated article text", source_label="Hoax"
            ),
        ]
        result = build_dedup_result(records, DedupConfig(shingle_size=3))
        self.assertTrue(all(record.label_conflict for record in result.records))
        self.assertEqual(result.report.conflict_record_count, 2)
        reasons = {entry.reason for entry in result.report.quarantine_entries}
        self.assertEqual(reasons, {"label_conflict_in_duplicate_component"})

    def test_report_never_contains_raw_text(self) -> None:
        records = [helpers.make_record(1, "unique synthetic marker text")]
        result = build_dedup_result(records, DedupConfig(shingle_size=3))
        payload = json.dumps(result.report.report_dict())
        self.assertNotIn("unique synthetic marker text", payload)


if __name__ == "__main__":
    unittest.main()
