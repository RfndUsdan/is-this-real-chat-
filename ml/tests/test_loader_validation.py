"""Loader and validation tests using synthetic fixtures only."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import helpers  # noqa: F401  (also sets up sys.path)

from hoaxscope_ml.data.errors import DatasetValidationError
from hoaxscope_ml.data.loader import LoadMetadata, RawDataset, load_mendeley_csv
from hoaxscope_ml.data.schema import (
    EXPECTED_CSV_FILENAME,
    EXPECTED_CSV_SHA256,
    map_source_label,
)
from hoaxscope_ml.data.validation import validate_dataset


class LoaderValidationTests(unittest.TestCase):
    def test_csv_parsing_and_cp1252_decoding(self) -> None:
        payload = (
            b"berita;tagging\r\n"
            b"synthetic \x92 quote;Valid\r\n"
            b"another synthetic article;Hoax\r\n"
        )
        with tempfile.TemporaryDirectory() as directory:
            path = helpers.write_cp1252_csv(Path(directory) / "synthetic.csv", payload)
            dataset = load_mendeley_csv(path)

        self.assertEqual(dataset.records[0].text, "synthetic ’ quote")
        self.assertEqual(dataset.records[0].source_label, "Valid")
        self.assertEqual(dataset.records[0].target_label, "not_flagged_as_hoax")
        self.assertEqual(dataset.records[1].target_label, "hoax")
        self.assertEqual(dataset.metadata.line_ending, "CRLF")

    def test_label_mapping_is_explicit(self) -> None:
        self.assertEqual(map_source_label("Valid"), "not_flagged_as_hoax")
        self.assertEqual(map_source_label("Hoax"), "hoax")
        self.assertNotEqual(map_source_label("Valid"), "true")
        self.assertNotEqual(map_source_label("Valid"), "verified")

    def test_unknown_label_is_blocked(self) -> None:
        payload = b"berita;tagging\r\nsynthetic text;Unknown\r\n"
        with tempfile.TemporaryDirectory() as directory:
            path = helpers.write_cp1252_csv(Path(directory) / "synthetic.csv", payload)
            with self.assertRaises(DatasetValidationError):
                load_mendeley_csv(path)

    def test_invalid_cp1252_byte_is_blocked(self) -> None:
        payload = b"berita;tagging\r\nsynthetic \x81 byte;Valid\r\n"
        with tempfile.TemporaryDirectory() as directory:
            path = helpers.write_cp1252_csv(Path(directory) / "synthetic.csv", payload)
            with self.assertRaises(DatasetValidationError):
                load_mendeley_csv(path)

    def test_missing_text_and_duplicate_are_reported(self) -> None:
        records = [
            helpers.make_record(1, "   "),
            helpers.make_record(2, "synthetic repeated text"),
            helpers.make_record(3, "synthetic   repeated text"),
        ]
        metadata = LoadMetadata(
            file_name=EXPECTED_CSV_FILENAME,
            bytes_count=100,
            sha256=EXPECTED_CSV_SHA256,
            encoding="cp1252",
            delimiter=";",
            header=("berita", "tagging"),
            line_ending="CRLF",
            utf8_bom_detected=False,
        )
        report = validate_dataset(RawDataset(records=records, metadata=metadata))
        codes = {issue.code for issue in report.issues}
        self.assertIn("empty_text", codes)
        self.assertIn("normalized_duplicate_text", codes)
        self.assertFalse(report.passed)


if __name__ == "__main__":
    unittest.main()
