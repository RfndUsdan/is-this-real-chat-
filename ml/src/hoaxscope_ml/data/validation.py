"""Blocking validation of the approved 600-news source dataset."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any

from ..text import has_invalid_control_chars, normalize_for_comparison
from .loader import EXPECTED_HEADER, RawDataset
from .schema import (
    EXPECTED_CSV_FILENAME,
    EXPECTED_CSV_SHA256,
    TARGET_LABELS,
    CanonicalRecord,
)

BASELINE_RECORD_COUNT = 600
BASELINE_SOURCE_LABEL_COUNTS: dict[str, int] = {"Hoax": 228, "Valid": 372}
BASELINE_EMPTY_TEXT_COUNT = 0
BASELINE_EXACT_DUPLICATE_COUNT = 0
BASELINE_NORMALIZED_DUPLICATE_COUNT = 0


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    """A blocking validation finding; messages never include raw text."""

    code: str
    message: str
    record_id: str | None = None

    def report_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "message": self.message,
            "record_id": self.record_id,
        }


@dataclass(frozen=True, slots=True)
class BaselineComparison:
    """One observed value compared with the Stage 2 baseline."""

    name: str
    expected: Any
    observed: Any
    matches: bool

    def report_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "expected": self.expected,
            "observed": self.observed,
            "matches": self.matches,
        }


@dataclass(frozen=True, slots=True)
class ValidationReport:
    """Report-safe validation result."""

    passed: bool
    metadata: dict[str, Any]
    record_count: int
    source_label_counts: dict[str, int]
    target_label_counts: dict[str, int]
    empty_text_count: int
    invalid_control_char_count: int
    exact_duplicate_count: int
    normalized_duplicate_count: int
    baseline_comparison: list[BaselineComparison]
    issues: list[ValidationIssue]

    def report_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "metadata": self.metadata,
            "record_count": self.record_count,
            "source_label_counts": self.source_label_counts,
            "target_label_counts": self.target_label_counts,
            "empty_text_count": self.empty_text_count,
            "invalid_control_char_count": self.invalid_control_char_count,
            "exact_duplicate_count": self.exact_duplicate_count,
            "normalized_duplicate_count": self.normalized_duplicate_count,
            "baseline_comparison": [
                item.report_dict() for item in self.baseline_comparison
            ],
            "issues": [issue.report_dict() for issue in self.issues],
        }


def _duplicate_count(values: list[str]) -> int:
    """Count records beyond the first occurrence of each repeated value."""
    return sum(count - 1 for count in Counter(values).values() if count > 1)


def _add_issue(
    issues: list[ValidationIssue],
    code: str,
    message: str,
    record_id: str | None = None,
) -> None:
    issues.append(ValidationIssue(code=code, message=message, record_id=record_id))


def validate_dataset(dataset: RawDataset) -> ValidationReport:
    """Run all blocking checks and return a report without raw text."""
    issues: list[ValidationIssue] = []
    records: list[CanonicalRecord] = dataset.records
    metadata = dataset.metadata

    if metadata.file_name != EXPECTED_CSV_FILENAME:
        _add_issue(
            issues,
            "unexpected_source_file",
            f"expected {EXPECTED_CSV_FILENAME!r}, got {metadata.file_name!r}",
        )
    if metadata.sha256 != EXPECTED_CSV_SHA256:
        _add_issue(
            issues,
            "sha256_mismatch",
            "source file SHA-256 does not match the frozen Stage 2 manifest",
        )
    if tuple(metadata.header) != EXPECTED_HEADER:
        _add_issue(
            issues,
            "missing_required_columns",
            f"expected header {list(EXPECTED_HEADER)}, got {list(metadata.header)}",
        )
    if metadata.utf8_bom_detected:
        _add_issue(issues, "encoding_bom", "UTF-8 BOM detected in a CP1252 source file")
    if metadata.encoding.lower() != "cp1252":
        _add_issue(issues, "encoding_mismatch", f"unexpected encoding {metadata.encoding!r}")

    source_label_counts = Counter(record.source_label for record in records)
    target_label_counts = Counter(record.target_label for record in records)
    empty_text_count = sum(1 for record in records if not record.text.strip())

    invalid_control_rows: list[str] = []
    invalid_type_rows: list[str] = []
    unknown_target_rows: list[str] = []
    for record in records:
        if has_invalid_control_chars(record.text):
            invalid_control_rows.append(record.record_id)
        if (
            not isinstance(record.record_id, str)
            or not isinstance(record.text, str)
            or not isinstance(record.source_label, str)
            or not isinstance(record.target_label, str)
            or not isinstance(record.source_dataset, str)
            or not isinstance(record.dataset_version, str)
            or not isinstance(record.source_row, int)
        ):
            invalid_type_rows.append(record.record_id)
        if record.target_label not in TARGET_LABELS:
            unknown_target_rows.append(record.record_id)

    for record_id in invalid_control_rows:
        _add_issue(
            issues,
            "invalid_control_char",
            "text contains an unsupported control character",
            record_id,
        )
    for record_id in invalid_type_rows:
        _add_issue(issues, "invalid_field_type", "canonical field has an unexpected type", record_id)
    for record_id in unknown_target_rows:
        _add_issue(issues, "unknown_target_label", "mapped target label is not canonical", record_id)

    exact_duplicate_count = _duplicate_count([record.text for record in records])
    normalized_duplicate_count = _duplicate_count(
        [normalize_for_comparison(record.text) for record in records]
    )

    if empty_text_count:
        _add_issue(issues, "empty_text", f"found {empty_text_count} empty or whitespace-only text fields")
    if exact_duplicate_count:
        _add_issue(issues, "exact_duplicate_text", f"found {exact_duplicate_count} exact duplicate records")
    if normalized_duplicate_count:
        _add_issue(
            issues,
            "normalized_duplicate_text",
            f"found {normalized_duplicate_count} duplicate records after Unicode/whitespace normalization",
        )

    comparison_values: list[tuple[str, Any, Any]] = [
        ("record_count", BASELINE_RECORD_COUNT, len(records)),
        ("source_label_counts", BASELINE_SOURCE_LABEL_COUNTS, dict(source_label_counts)),
        ("empty_text_count", BASELINE_EMPTY_TEXT_COUNT, empty_text_count),
        ("exact_duplicate_count", BASELINE_EXACT_DUPLICATE_COUNT, exact_duplicate_count),
        (
            "normalized_duplicate_count",
            BASELINE_NORMALIZED_DUPLICATE_COUNT,
            normalized_duplicate_count,
        ),
    ]
    baseline_comparison = [
        BaselineComparison(
            name=name,
            expected=expected,
            observed=observed,
            matches=expected == observed,
        )
        for name, expected, observed in comparison_values
    ]
    for comparison in baseline_comparison:
        if not comparison.matches:
            _add_issue(
                issues,
                "baseline_discrepancy",
                f"baseline mismatch for {comparison.name}: "
                f"expected {comparison.expected!r}, observed {comparison.observed!r}",
            )

    return ValidationReport(
        passed=not issues,
        metadata=metadata.report_dict(),
        record_count=len(records),
        source_label_counts=dict(sorted(source_label_counts.items())),
        target_label_counts=dict(sorted(target_label_counts.items())),
        empty_text_count=empty_text_count,
        invalid_control_char_count=len(invalid_control_rows),
        exact_duplicate_count=exact_duplicate_count,
        normalized_duplicate_count=normalized_duplicate_count,
        baseline_comparison=baseline_comparison,
        issues=issues,
    )
