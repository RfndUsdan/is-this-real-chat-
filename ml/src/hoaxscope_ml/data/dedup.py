"""URL grouping, near-duplicate detection, and conflict quarantine.

URL relationships and text-similarity relationships are detected separately,
then merged with connected components. Duplicate records are marked, not
deleted. Reports never contain raw text or URLs.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any

from ..text import alphanumeric_tokens, jaccard, word_shingles
from .schema import CanonicalRecord
from .workbook import WorkbookAudit


@dataclass(frozen=True, slots=True)
class DedupConfig:
    """Deterministic parameters for near-duplicate detection."""

    shingle_size: int = 5
    similarity_threshold: float = 0.5
    min_length_ratio: float = 0.2

    def report_dict(self) -> dict[str, Any]:
        return {
            "shingle_size": self.shingle_size,
            "similarity_threshold": self.similarity_threshold,
            "min_length_ratio": self.min_length_ratio,
            "similarity_metric": "jaccard_on_word_shingles",
        }


class DisjointSet:
    """Small deterministic union-find for transitive connected components."""

    def __init__(self, size: int) -> None:
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, item: int) -> int:
        while self.parent[item] != item:
            self.parent[item] = self.parent[self.parent[item]]
            item = self.parent[item]
        return item

    def union(self, left: int, right: int) -> None:
        left_root, right_root = self.find(left), self.find(right)
        if left_root == right_root:
            return
        if self.rank[left_root] < self.rank[right_root]:
            left_root, right_root = right_root, left_root
        self.parent[right_root] = left_root
        if self.rank[left_root] == self.rank[right_root]:
            self.rank[left_root] += 1

    def groups(self) -> list[list[int]]:
        buckets: dict[int, list[int]] = {}
        for index in range(len(self.parent)):
            buckets.setdefault(self.find(index), []).append(index)
        return [sorted(bucket) for bucket in sorted(buckets.values(), key=lambda b: b[0])]


def attach_url_group_ids(
    records: list[CanonicalRecord], audit: WorkbookAudit
) -> list[CanonicalRecord]:
    """Attach opaque URL group IDs from the row-order workbook audit."""
    return [
        record.with_url_group(
            audit.rows[record.source_row].url_group_id
            if record.source_row in audit.rows
            else None
        )
        for record in records
    ]


def url_groups(records: list[CanonicalRecord]) -> dict[str, list[int]]:
    """Group records by opaque URL group ID; records without a URL are skipped."""
    groups: dict[str, list[int]] = {}
    for index, record in enumerate(records):
        if record.url_group_id:
            groups.setdefault(record.url_group_id, []).append(index)
    return groups


def find_near_duplicate_pairs(
    records: list[CanonicalRecord], config: DedupConfig
) -> list[tuple[int, int]]:
    """Find candidate near-duplicate index pairs using deterministic shingles."""
    shingles = [
        word_shingles(alphanumeric_tokens(record.text), config.shingle_size)
        for record in records
    ]
    lengths = [len(alphanumeric_tokens(record.text)) for record in records]
    pairs: list[tuple[int, int]] = []
    for left in range(len(records)):
        for right in range(left + 1, len(records)):
            longest = max(lengths[left], lengths[right])
            if longest == 0:
                continue
            if min(lengths[left], lengths[right]) / longest < config.min_length_ratio:
                continue
            if jaccard(shingles[left], shingles[right]) >= config.similarity_threshold:
                pairs.append((left, right))
    return pairs


@dataclass(frozen=True, slots=True)
class ComponentReport:
    """Report-safe description of a duplicate component."""

    component_id: str
    size: int
    record_ids: list[str]
    target_label_counts: dict[str, int]
    has_label_conflict: bool

    def report_dict(self) -> dict[str, Any]:
        return {
            "component_id": self.component_id,
            "size": self.size,
            "record_ids": self.record_ids,
            "target_label_counts": self.target_label_counts,
            "has_label_conflict": self.has_label_conflict,
        }


@dataclass(frozen=True, slots=True)
class QuarantineEntry:
    """Report-safe quarantine reason; no raw text or URL is included."""

    record_id: str
    component_id: str
    reason: str

    def report_dict(self) -> dict[str, Any]:
        return {
            "record_id": self.record_id,
            "component_id": self.component_id,
            "reason": self.reason,
        }


@dataclass(frozen=True, slots=True)
class DedupReport:
    """Report-safe deduplication summary."""

    config: dict[str, Any]
    url_unique_count: int
    url_duplicate_group_count: int
    url_duplicate_row_count: int
    near_duplicate_candidate_pairs: int
    near_duplicate_component_count: int
    near_duplicate_component_sizes: list[int]
    largest_near_duplicate_component: int
    near_duplicate_conflict_component_count: int
    duplicate_component_count: int
    multi_record_component_count: int
    singleton_component_count: int
    component_sizes: list[int]
    components: list[ComponentReport]
    conflict_component_count: int
    conflict_record_count: int
    quarantine_entries: list[QuarantineEntry]

    def report_dict(self) -> dict[str, Any]:
        return {
            "config": self.config,
            "url_unique_count": self.url_unique_count,
            "url_duplicate_group_count": self.url_duplicate_group_count,
            "url_duplicate_row_count": self.url_duplicate_row_count,
            "near_duplicate_candidate_pairs": self.near_duplicate_candidate_pairs,
            "near_duplicate_component_count": self.near_duplicate_component_count,
            "near_duplicate_component_sizes": self.near_duplicate_component_sizes,
            "largest_near_duplicate_component": self.largest_near_duplicate_component,
            "near_duplicate_conflict_component_count": self.near_duplicate_conflict_component_count,
            "duplicate_component_count": self.duplicate_component_count,
            "multi_record_component_count": self.multi_record_component_count,
            "singleton_component_count": self.singleton_component_count,
            "component_sizes": self.component_sizes,
            "components": [item.report_dict() for item in self.components],
            "conflict_component_count": self.conflict_component_count,
            "conflict_record_count": self.conflict_record_count,
            "quarantine_entries": [item.report_dict() for item in self.quarantine_entries],
        }


@dataclass(frozen=True, slots=True)
class DedupResult:
    """Canonical records with grouping metadata plus report-safe artifacts."""

    records: list[CanonicalRecord]
    report: DedupReport
    near_duplicate_pairs: list[tuple[int, int]]


def _component_id(records: list[CanonicalRecord], group: list[int]) -> str:
    first_row = min(records[index].source_row for index in group)
    return f"dup-r{first_row:04d}"


def _label_counts(records: list[CanonicalRecord], group: list[int]) -> dict[str, int]:
    return dict(sorted(Counter(records[index].target_label for index in group).items()))


def build_dedup_result(
    records: list[CanonicalRecord],
    config: DedupConfig | None = None,
) -> DedupResult:
    """Merge URL and near-duplicate relationships into final components."""
    config = config or DedupConfig()
    total = len(records)
    url_groups_map = url_groups(records)
    near_pairs = find_near_duplicate_pairs(records, config)

    near_set = DisjointSet(total)
    for left, right in near_pairs:
        near_set.union(left, right)
    near_components = [group for group in near_set.groups() if len(group) > 1]
    near_sizes = sorted((len(group) for group in near_components), reverse=True)
    near_conflicts = sum(
        1
        for group in near_components
        if len(_label_counts(records, group)) > 1
    )

    merged = DisjointSet(total)
    for group in url_groups_map.values():
        for index in group[1:]:
            merged.union(group[0], index)
    for left, right in near_pairs:
        merged.union(left, right)

    final_groups = merged.groups()
    component_ids = {
        index: _component_id(records, group)
        for group in final_groups
        for index in group
    }
    conflict_groups = {
        component_ids[group[0]]
        for group in final_groups
        if len(_label_counts(records, group)) > 1
    }

    updated: list[CanonicalRecord] = []
    quarantine_entries: list[QuarantineEntry] = []
    component_reports: list[ComponentReport] = []
    for index, record in enumerate(records):
        component_id = component_ids[index]
        conflict = component_id in conflict_groups
        updated.append(
            record.with_grouping(
                duplicate_group_id=component_id,
                label_conflict=conflict,
            )
        )
        if conflict:
            quarantine_entries.append(
                QuarantineEntry(
                    record_id=record.record_id,
                    component_id=component_id,
                    reason="label_conflict_in_duplicate_component",
                )
            )

    for group in final_groups:
        if len(group) < 2:
            continue
        component_id = component_ids[group[0]]
        component_reports.append(
            ComponentReport(
                component_id=component_id,
                size=len(group),
                record_ids=[records[index].record_id for index in group],
                target_label_counts=_label_counts(records, group),
                has_label_conflict=component_id in conflict_groups,
            )
        )

    report = DedupReport(
        config=config.report_dict(),
        url_unique_count=len(url_groups_map),
        url_duplicate_group_count=sum(1 for group in url_groups_map.values() if len(group) > 1),
        url_duplicate_row_count=sum(
            len(group) for group in url_groups_map.values() if len(group) > 1
        ),
        near_duplicate_candidate_pairs=len(near_pairs),
        near_duplicate_component_count=len(near_components),
        near_duplicate_component_sizes=near_sizes,
        largest_near_duplicate_component=near_sizes[0] if near_sizes else 0,
        near_duplicate_conflict_component_count=near_conflicts,
        duplicate_component_count=len(final_groups),
        multi_record_component_count=sum(1 for group in final_groups if len(group) > 1),
        singleton_component_count=sum(1 for group in final_groups if len(group) == 1),
        component_sizes=sorted((len(group) for group in final_groups), reverse=True),
        components=component_reports,
        conflict_component_count=len(conflict_groups),
        conflict_record_count=len(quarantine_entries),
        quarantine_entries=quarantine_entries,
    )
    return DedupResult(
        records=updated,
        report=report,
        near_duplicate_pairs=near_pairs,
    )
