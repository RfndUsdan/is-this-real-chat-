"""Canonical schema for the HoaxScope Stage 3 data pipeline.

The canonical record keeps the source label and the mapped target label
separate. ``record_id`` is derived from the frozen source row position, not
from raw text, so it can safely appear in reports.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

SOURCE_DATASET = "mendeley_p3hfgr5j3m"
DATASET_VERSION = "1"
EXPECTED_CSV_FILENAME = "600 news with valid hoax label.csv"
EXPECTED_WORKBOOK_FILENAME = "600 news labelling process.xlsx"
EXPECTED_CSV_SHA256 = (
    "8c16f1e6258f3a828381c0e4b12ecee6730111c7c5be95ef5e70725201631f67"
)
EXPECTED_WORKBOOK_SHA256 = (
    "ab2b269cf5df8068a11a8e823b8db55ca5f15671da7ea41699848fda0816c28a"
)

SOURCE_LABEL_TO_TARGET: dict[str, str] = {
    "Hoax": "hoax",
    "Valid": "not_flagged_as_hoax",
}

TARGET_LABELS: frozenset[str] = frozenset(SOURCE_LABEL_TO_TARGET.values())
SPLIT_NAMES: tuple[str, ...] = ("train", "validation", "test")


@dataclass(frozen=True, slots=True)
class CanonicalRecord:
    """One source row converted to the HoaxScope canonical schema.

    ``text`` holds raw source text and must never be written to reports or
    committed fixtures. ``split`` is derived later by the split stage.
    """

    record_id: str
    source_row: int
    text: str
    source_label: str
    target_label: str
    source_dataset: str
    dataset_version: str
    url_group_id: str | None = None
    duplicate_group_id: str | None = None
    label_conflict: bool = False
    split: str | None = None

    def with_url_group(self, url_group_id: str | None) -> "CanonicalRecord":
        """Return a copy with an opaque URL group identifier."""
        return CanonicalRecord(
            record_id=self.record_id,
            source_row=self.source_row,
            text=self.text,
            source_label=self.source_label,
            target_label=self.target_label,
            source_dataset=self.source_dataset,
            dataset_version=self.dataset_version,
            url_group_id=url_group_id,
            duplicate_group_id=self.duplicate_group_id,
            label_conflict=self.label_conflict,
            split=self.split,
        )

    def with_grouping(
        self,
        *,
        duplicate_group_id: str,
        label_conflict: bool,
    ) -> "CanonicalRecord":
        """Return a copy with duplicate-group metadata applied."""
        return CanonicalRecord(
            record_id=self.record_id,
            source_row=self.source_row,
            text=self.text,
            source_label=self.source_label,
            target_label=self.target_label,
            source_dataset=self.source_dataset,
            dataset_version=self.dataset_version,
            url_group_id=self.url_group_id,
            duplicate_group_id=duplicate_group_id,
            label_conflict=label_conflict,
            split=self.split,
        )

    def with_split(self, split: str) -> "CanonicalRecord":
        """Return a copy assigned to a split."""
        if split not in SPLIT_NAMES:
            raise ValueError(f"unknown split name: {split}")
        return CanonicalRecord(
            record_id=self.record_id,
            source_row=self.source_row,
            text=self.text,
            source_label=self.source_label,
            target_label=self.target_label,
            source_dataset=self.source_dataset,
            dataset_version=self.dataset_version,
            url_group_id=self.url_group_id,
            duplicate_group_id=self.duplicate_group_id,
            label_conflict=self.label_conflict,
            split=split,
        )

    def report_dict(self) -> dict[str, Any]:
        """Return report-safe metadata; raw text is deliberately excluded."""
        return {
            "record_id": self.record_id,
            "source_row": self.source_row,
            "source_label": self.source_label,
            "target_label": self.target_label,
            "source_dataset": self.source_dataset,
            "dataset_version": self.dataset_version,
            "url_group_id": self.url_group_id,
            "duplicate_group_id": self.duplicate_group_id,
            "label_conflict": self.label_conflict,
            "split": self.split,
        }


def make_record_id(source_row: int) -> str:
    """Build a stable ID from source row position, never from text content."""
    if source_row < 2:
        raise ValueError("source_row must be a 1-based CSV row including header")
    return f"{SOURCE_DATASET}:v{DATASET_VERSION}:row:{source_row}"


def map_source_label(label: str) -> str:
    """Map a frozen source label to the canonical target label."""
    try:
        return SOURCE_LABEL_TO_TARGET[label]
    except KeyError as exc:
        raise KeyError(f"unknown source label: {label!r}") from exc
