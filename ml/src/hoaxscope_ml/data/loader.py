"""CSV loader for the approved Mendeley 600-news source file.

The loader is intentionally strict: it decodes CP1252 with ``errors='strict'``
and refuses malformed rows instead of guessing. It never writes raw text to
reports.
"""

from __future__ import annotations

import csv
import hashlib
import io
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .errors import DatasetValidationError
from .schema import (
    DATASET_VERSION,
    SOURCE_DATASET,
    map_source_label,
    make_record_id,
)

EXPECTED_HEADER: tuple[str, ...] = ("berita", "tagging")
ENCODING = "cp1252"
DELIMITER = ";"
UTF8_BOM = b"\xef\xbb\xbf"


@dataclass(frozen=True, slots=True)
class LoadMetadata:
    """Report-safe metadata about the loaded source file."""

    file_name: str
    bytes_count: int
    sha256: str
    encoding: str
    delimiter: str
    header: tuple[str, ...]
    line_ending: str
    utf8_bom_detected: bool

    def report_dict(self) -> dict[str, Any]:
        return {
            "file_name": self.file_name,
            "bytes_count": self.bytes_count,
            "sha256": self.sha256,
            "encoding": self.encoding,
            "delimiter": self.delimiter,
            "header": list(self.header),
            "line_ending": self.line_ending,
            "utf8_bom_detected": self.utf8_bom_detected,
        }


@dataclass(frozen=True, slots=True)
class RawDataset:
    """Loaded canonical records plus report-safe file metadata."""

    records: list[CanonicalRecord]
    metadata: LoadMetadata


def sha256_bytes(payload: bytes) -> str:
    """Return the SHA-256 hex digest of ``payload``."""
    return hashlib.sha256(payload).hexdigest()


def detect_line_ending(payload: bytes) -> str:
    """Classify the dominant line ending without decoding text."""
    crlf = payload.count(b"\r\n")
    lone_lf = payload.count(b"\n") - crlf
    lone_cr = payload.count(b"\r") - crlf
    # CRLF counts row separators; lone LF bytes may occur inside quoted text.
    if crlf:
        return "CRLF"
    if lone_lf:
        return "LF"
    if lone_cr:
        return "CR"
    return "none"


def load_mendeley_csv(path: str | Path) -> RawDataset:
    """Load and minimally validate the approved 600-news CSV."""
    source = Path(path)
    if not source.is_file():
        raise DatasetValidationError(f"dataset file not found: {source.name}")

    payload = source.read_bytes()
    try:
        decoded = payload.decode(ENCODING, errors="strict")
    except UnicodeDecodeError as exc:
        raise DatasetValidationError(
            f"file is not valid {ENCODING}: invalid byte at position {exc.start}"
        ) from exc

    reader = csv.reader(
        io.StringIO(decoded, newline=""),
        delimiter=DELIMITER,
        strict=True,
    )
    try:
        header = tuple(next(reader))
    except StopIteration as exc:
        raise DatasetValidationError("CSV is empty; expected a header row") from exc
    except csv.Error as exc:
        raise DatasetValidationError(f"malformed CSV header: {exc}") from exc

    if header != EXPECTED_HEADER:
        raise DatasetValidationError(
            f"unexpected header: expected {list(EXPECTED_HEADER)}, got {list(header)}"
        )

    from .schema import CanonicalRecord  # local import keeps schema/loader cycle small

    records: list[CanonicalRecord] = []
    try:
        for row_number, row in enumerate(reader, start=2):
            if len(row) != 2:
                raise DatasetValidationError(
                    f"row {row_number} has {len(row)} columns; expected 2"
                )
            text, source_label = row
            try:
                target_label = map_source_label(source_label)
            except KeyError as exc:
                raise DatasetValidationError(
                    f"row {row_number} has unknown source label {source_label!r}"
                ) from exc
            records.append(
                CanonicalRecord(
                    record_id=make_record_id(row_number),
                    source_row=row_number,
                    text=text,
                    source_label=source_label,
                    target_label=target_label,
                    source_dataset=SOURCE_DATASET,
                    dataset_version=DATASET_VERSION,
                )
            )
    except csv.Error as exc:
        raise DatasetValidationError(f"malformed CSV row: {exc}") from exc

    metadata = LoadMetadata(
        file_name=source.name,
        bytes_count=len(payload),
        sha256=sha256_bytes(payload),
        encoding=ENCODING,
        delimiter=DELIMITER,
        header=header,
        line_ending=detect_line_ending(payload),
        utf8_bom_detected=payload.startswith(UTF8_BOM),
    )
    return RawDataset(records=records, metadata=metadata)
