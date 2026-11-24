"""Synthetic fixtures for Stage 3 tests. No raw dataset content is used."""

from __future__ import annotations

import sys
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from hoaxscope_ml.data.schema import (  # noqa: E402
    DATASET_VERSION,
    SOURCE_DATASET,
    CanonicalRecord,
    map_source_label,
    make_record_id,
)


def write_cp1252_csv(path: Path, payload: bytes) -> Path:
    """Write a tiny synthetic CP1252 CSV fixture."""
    path.write_bytes(payload)
    return path


def make_record(
    data_row: int,
    text: str,
    *,
    source_label: str = "Valid",
    url_group_id: str | None = None,
    duplicate_group_id: str | None = None,
    label_conflict: bool = False,
) -> CanonicalRecord:
    """Build a synthetic canonical record with a row-based ID."""
    source_row = data_row + 1
    return CanonicalRecord(
        record_id=make_record_id(source_row),
        source_row=source_row,
        text=text,
        source_label=source_label,
        target_label=map_source_label(source_label),
        source_dataset=SOURCE_DATASET,
        dataset_version=DATASET_VERSION,
        url_group_id=url_group_id,
        duplicate_group_id=duplicate_group_id,
        label_conflict=label_conflict,
    )


def write_minimal_workbook(path: Path, rows: list[tuple[str, str]]) -> Path:
    """Create a minimal XLSX with URL in column C and vote in column G."""
    strings: list[str] = []
    lookup: dict[str, int] = {}

    def string_index(value: str) -> int:
        if value not in lookup:
            lookup[value] = len(strings)
            strings.append(value)
        return lookup[value]

    def cell(reference: str, value: str) -> str:
        return f'<c r="{reference}" t="s"><v>{string_index(value)}</v></c>'

    sheet_rows = ['<row r="1">' + cell("C1", "Link") + cell("G1", "Voting") + "</row>"]
    for offset, (url, vote) in enumerate(rows, start=2):
        sheet_rows.append(
            f'<row r="{offset}">' + cell(f"C{offset}", url) + cell(f"G{offset}", vote) + "</row>"
        )

    shared = "".join(f"<si><t>{escape(value)}</t></si>" for value in strings)
    ns = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr(
            "xl/workbook.xml",
            f'<workbook xmlns="{ns}"><sheets>'
            '<sheet name="KW1" sheetId="1"/></sheets></workbook>',
        )
        archive.writestr(
            "xl/sharedStrings.xml",
            f'<sst xmlns="{ns}" count="{len(strings)}" uniqueCount="{len(strings)}">'
            f"{shared}</sst>",
        )
        archive.writestr(
            "xl/worksheets/sheet1.xml",
            f'<worksheet xmlns="{ns}"><sheetData>{"".join(sheet_rows)}</sheetData></worksheet>',
        )
    return path
