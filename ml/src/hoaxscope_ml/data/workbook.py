"""Row-order workbook audit for URLs and voting metadata.

The workbook has no official join key to the CSV. The mapping implemented
here is an audit inference: 12 sheets of nominally 50 rows are read in sheet
order and URL cells in column C are assigned sequentially to CSV data rows.
It must never be treated as an official record relation.
"""

from __future__ import annotations

import hashlib
import re
import zipfile
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

from .errors import DatasetValidationError
from .schema import EXPECTED_WORKBOOK_FILENAME, EXPECTED_WORKBOOK_SHA256

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
MAPPING_METHOD = "row_order_inference_12x50"
MAPPING_WARNING = (
    "Workbook-to-CSV mapping is a row-order audit inference, not an official relation."
)
URL_COLUMN = "C"
VOTE_COLUMN = "G"
RATER_COLUMNS = ("D", "E", "F")


@dataclass(frozen=True, slots=True)
class WorkbookRow:
    """Internal audit row; URLs are never included in reports."""

    source_row: int
    sheet_name: str
    sheet_row: int
    url: str
    vote: str

    @property
    def url_group_id(self) -> str:
        """Opaque group key; the raw URL is never written to reports."""
        return url_group_id(self.url)

    @property
    def majority_vote(self) -> str | None:
        """Workbook's recorded final vote (column G), not rater aggregation."""
        return self.vote.lower() if self.vote else None


@dataclass(frozen=True, slots=True)
class WorkbookAudit:
    """Report-safe workbook audit result."""

    rows: dict[int, WorkbookRow]
    mapped_count: int
    missing_count: int
    unique_url_count: int
    duplicate_url_group_count: int
    duplicate_url_row_count: int
    vote_disagreement_count: int
    sheet_count: int
    sha256: str
    manifest_verified: bool = True

    def report_dict(self) -> dict[str, Any]:
        return {
            "mapping_method": MAPPING_METHOD,
            "manifest_verified": self.manifest_verified,
            "warning": MAPPING_WARNING,
            "sheet_count": self.sheet_count,
            "sha256": self.sha256,
            "mapped_count": self.mapped_count,
            "missing_count": self.missing_count,
            "unique_url_count": self.unique_url_count,
            "duplicate_url_group_count": self.duplicate_url_group_count,
            "duplicate_url_row_count": self.duplicate_url_row_count,
            "vote_disagreement_count": self.vote_disagreement_count,
        }


def sha256_file(path: str | Path) -> str:
    """Return SHA-256 of a local file."""
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def url_group_id(url: str) -> str:
    """Return an opaque deterministic group ID without exposing the URL."""
    digest = hashlib.sha256(url.strip().encode("utf-8")).hexdigest()[:12]
    return f"url-{digest}"


def _column_letters(cell_ref: str) -> str:
    return "".join(char for char in cell_ref if char.isalpha())


def _looks_like_url(value: str) -> bool:
    """Detect URLs with or without scheme while excluding headers/topics."""
    lowered = value.lower()
    if "http" in lowered or "www." in lowered:
        return True
    return "/" in value and bool(re.search(r"[a-z0-9-]+\.[a-z]{2,}", lowered))


def _shared_strings(archive: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in archive.namelist():
        return []
    root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
    return [
        "".join(node.text or "" for node in item.iter(f"{{{NS['m']}}}t"))
        for item in root.findall("m:si", NS)
    ]


def _cell_value(cell: ET.Element, strings: list[str]) -> str:
    kind = cell.get("t")
    if kind == "inlineStr":
        return "".join(node.text or "" for node in cell.iter(f"{{{NS['m']}}}t")).strip()
    value = cell.find("m:v", NS)
    if value is None or value.text is None:
        return ""
    if kind == "s":
        index = int(value.text)
        return strings[index].strip() if 0 <= index < len(strings) else ""
    return value.text.strip()


def _sheet_values(archive: zipfile.ZipFile, sheet_path: str) -> list[tuple[int, dict[str, str]]]:
    strings = _shared_strings(archive)
    root = ET.fromstring(archive.read(sheet_path))
    rows: list[tuple[int, dict[str, str]]] = []
    for row in root.findall(".//m:sheetData/m:row", NS):
        try:
            row_number = int(row.get("r", "0"))
        except ValueError:
            continue
        values = {
            _column_letters(cell.get("r", "")): _cell_value(cell, strings)
            for cell in row.findall("m:c", NS)
        }
        rows.append((row_number, values))
    return sorted(rows, key=lambda item: item[0])


def _sheet_names(archive: zipfile.ZipFile) -> list[str]:
    root = ET.fromstring(archive.read("xl/workbook.xml"))
    return [sheet.get("name", "") for sheet in root.findall(".//m:sheet", NS)]


def load_workbook_audit(
    path: str | Path,
    *,
    source_labels: dict[int, str] | None = None,
    verify_manifest: bool = True,
) -> WorkbookAudit:
    """Read URL/vote metadata from the workbook using row-order inference."""
    source = Path(path)
    if not source.is_file():
        raise DatasetValidationError(f"workbook file not found: {source.name}")
    if verify_manifest and source.name != EXPECTED_WORKBOOK_FILENAME:
        raise DatasetValidationError(f"unexpected workbook name: {source.name}")

    digest = sha256_file(source)
    if verify_manifest and digest != EXPECTED_WORKBOOK_SHA256:
        raise DatasetValidationError("workbook SHA-256 does not match the frozen Stage 2 manifest")

    with zipfile.ZipFile(source) as archive:
        names = _sheet_names(archive)
        candidates: list[tuple[str, int, str, str]] = []
        for index, sheet_name in enumerate(names, start=1):
            sheet_path = f"xl/worksheets/sheet{index}.xml"
            if sheet_path not in archive.namelist():
                continue
            for sheet_row, values in _sheet_values(archive, sheet_path):
                url = values.get(URL_COLUMN, "")
                if _looks_like_url(url):
                    vote = values.get(VOTE_COLUMN, "")
                    candidates.append((sheet_name, sheet_row, url, vote))

    rows: dict[int, WorkbookRow] = {}
    for offset, (sheet_name, sheet_row, url, vote) in enumerate(candidates):
        source_row = offset + 2
        if source_row > 602:
            break
        rows[source_row] = WorkbookRow(
            source_row=source_row,
            sheet_name=sheet_name,
            sheet_row=sheet_row,
            url=url,
            vote=vote,
        )

    url_counter = Counter(url_group_id(row.url) for row in rows.values())
    disagreement = 0
    if source_labels:
        for source_row, row in rows.items():
            vote = row.majority_vote
            csv_label = source_labels.get(source_row)
            if vote is None or csv_label is None:
                continue
            if SOURCE_TO_VOTE.get(csv_label, csv_label) != vote.lower():
                disagreement += 1

    return WorkbookAudit(
        rows=rows,
        mapped_count=len(rows),
        missing_count=max(0, 600 - len(rows)),
        unique_url_count=len(url_counter),
        duplicate_url_group_count=sum(1 for count in url_counter.values() if count > 1),
        duplicate_url_row_count=sum(count for count in url_counter.values() if count > 1),
        vote_disagreement_count=disagreement,
        sheet_count=len(names),
        sha256=digest,
        manifest_verified=verify_manifest,
    )


SOURCE_TO_VOTE: dict[str, str] = {"Valid": "valid", "Hoax": "hoax"}
