"""Workbook row-order audit tests using synthetic XLSX fixtures only."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import helpers  # noqa: F401

from hoaxscope_ml.data.errors import DatasetValidationError
from hoaxscope_ml.data.workbook import load_workbook_audit


class WorkbookTests(unittest.TestCase):
    def test_row_order_url_mapping_and_vote_audit(self) -> None:
        rows = [
            ("https://example.invalid/a", "valid"),
            ("https://example.invalid/a", "hoax"),
            ("https://example.invalid/b", "valid"),
        ]
        labels = {2: "Valid", 3: "Hoax", 4: "Hoax"}
        with tempfile.TemporaryDirectory() as directory:
            path = helpers.write_minimal_workbook(Path(directory) / "synthetic.xlsx", rows)
            audit = load_workbook_audit(
                path, source_labels=labels, verify_manifest=False
            )

        report = audit.report_dict()
        self.assertEqual(report["mapped_count"], 3)
        self.assertEqual(report["unique_url_count"], 2)
        self.assertEqual(report["duplicate_url_group_count"], 1)
        self.assertEqual(report["duplicate_url_row_count"], 2)
        self.assertEqual(report["vote_disagreement_count"], 1)
        self.assertIn("row-order audit inference", report["warning"])
        self.assertEqual(audit.rows[2].url_group_id, audit.rows[3].url_group_id)

    def test_manifest_check_can_be_enforced(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = helpers.write_minimal_workbook(
                Path(directory) / "wrong-name.xlsx",
                [("https://example.invalid/a", "valid")],
            )
            with self.assertRaises(DatasetValidationError):
                load_workbook_audit(path, verify_manifest=True)


if __name__ == "__main__":
    unittest.main()
