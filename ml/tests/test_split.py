"""Group-aware split tests using synthetic fixtures only."""

from __future__ import annotations

import unittest

import helpers  # noqa: F401

from hoaxscope_ml.data.split import SplitConfig, make_split, validate_split


def _grouped(index: int, label: str, group: str) -> object:
    base = helpers.make_record(index, f"synthetic article {index}", source_label=label)
    return base.with_grouping(duplicate_group_id=group, label_conflict=False)


class SplitTests(unittest.TestCase):
    def test_group_aware_split(self) -> None:
        records = [
            _grouped(index, "Valid" if index % 2 == 0 else "Hoax", f"g{index}")
            for index in range(1, 9)
        ]
        result = make_split(records, [], SplitConfig(seed=7))
        self.assertTrue(result.report.passed)
        self.assertEqual(len(result.report.assignments), len(records))

        group_splits: dict[str, set[str]] = {}
        for record in result.records:
            group_splits.setdefault(record.duplicate_group_id or "", set()).add(
                record.split or ""
            )
        self.assertTrue(all(len(splits) == 1 for splits in group_splits.values()))

    def test_leakage_validation_detects_group_leak(self) -> None:
        records = [_grouped(1, "Valid", "g1"), _grouped(2, "Hoax", "g1")]
        assignments = {0: "train", 1: "test"}
        checks = validate_split(records, assignments, [])
        failed = {check.name for check in checks if not check.passed}
        self.assertIn("duplicate_component_leakage", failed)

    def test_reproducibility(self) -> None:
        records = [
            _grouped(index, "Valid" if index % 3 else "Hoax", f"g{index}")
            for index in range(1, 10)
        ]
        first = make_split(records, [], SplitConfig(seed=42))
        second = make_split(records, [], SplitConfig(seed=42))
        self.assertEqual(first.report.assignments, second.report.assignments)

    def test_quarantined_records_are_excluded(self) -> None:
        records = [_grouped(index, "Valid", f"g{index}") for index in range(1, 8)]
        records.append(
            helpers.make_record(8, "conflict", source_label="Hoax").with_grouping(
                duplicate_group_id="g8", label_conflict=True
            )
        )
        result = make_split(records, [], SplitConfig(seed=11))
        self.assertEqual(result.report.quarantined_record_count, 1)
        self.assertNotIn(records[-1].record_id, result.report.assignments)
        self.assertIsNone(result.records[-1].split)


if __name__ == "__main__":
    unittest.main()
