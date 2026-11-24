"""Group-aware, deterministic train/validation/test splitting.

Every duplicate component is assigned as a whole. Ratios are targets, not
constraints: if group distribution prevents a close match, the closest valid
assignment is kept and reported. An invalid split is never returned.
"""

from __future__ import annotations

import random
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Any

from ..text import normalize_for_comparison
from .errors import SplitImpossibleError
from .schema import SPLIT_NAMES, TARGET_LABELS, CanonicalRecord


@dataclass(frozen=True, slots=True)
class SplitConfig:
    """Split configuration with a fixed seed for reproducibility."""

    seed: int = 20261124
    train_ratio: float = 0.70
    validation_ratio: float = 0.15
    test_ratio: float = 0.15

    @property
    def ratios(self) -> dict[str, float]:
        return {
            "train": self.train_ratio,
            "validation": self.validation_ratio,
            "test": self.test_ratio,
        }

    def report_dict(self) -> dict[str, Any]:
        return {
            "seed": self.seed,
            **self.ratios,
            "strategy": "group_aware_greedy_stratified",
        }


@dataclass(frozen=True, slots=True)
class LeakageCheck:
    """Result of one independent leakage check."""

    name: str
    passed: bool
    detail: str

    def report_dict(self) -> dict[str, Any]:
        return {"name": self.name, "passed": self.passed, "detail": self.detail}


@dataclass(frozen=True, slots=True)
class SplitReport:
    """Report-safe split summary; no raw text or URLs."""

    config: dict[str, Any]
    passed: bool
    eligible_record_count: int
    quarantined_record_count: int
    group_count: int
    groups_by_split: dict[str, int]
    record_counts_by_split: dict[str, int]
    label_counts_by_split: dict[str, dict[str, int]]
    target_label_counts_by_split: dict[str, dict[str, int]]
    assignments: dict[str, str]
    leakage_checks: list[LeakageCheck]

    def report_dict(self) -> dict[str, Any]:
        return {
            "config": self.config,
            "passed": self.passed,
            "eligible_record_count": self.eligible_record_count,
            "quarantined_record_count": self.quarantined_record_count,
            "group_count": self.group_count,
            "groups_by_split": self.groups_by_split,
            "record_counts_by_split": self.record_counts_by_split,
            "label_counts_by_split": self.label_counts_by_split,
            "target_label_counts_by_split": self.target_label_counts_by_split,
            "assignments": self.assignments,
            "leakage_checks": [check.report_dict() for check in self.leakage_checks],
        }


@dataclass(frozen=True, slots=True)
class SplitResult:
    """Canonical records with split assignments plus the audit report."""

    records: list[CanonicalRecord]
    report: SplitReport


def _integer_targets(
    total_by_label: dict[str, int], config: SplitConfig
) -> dict[str, dict[str, int]]:
    """Convert target ratios to integer label counts that sum to the total."""
    targets = {split: {label: 0 for label in total_by_label} for split in SPLIT_NAMES}
    for label, total in total_by_label.items():
        train = round(total * config.train_ratio)
        validation = round(total * config.validation_ratio)
        targets["train"][label] = train
        targets["validation"][label] = validation
        targets["test"][label] = total - train - validation
    return targets


def validate_split(
    records: list[CanonicalRecord],
    assignments: dict[int, str],
    near_pairs: list[tuple[int, int]],
) -> list[LeakageCheck]:
    """Run independent leakage checks; assignments use record indices."""
    checks: list[LeakageCheck] = []
    eligible = {
        index
        for index, record in enumerate(records)
        if not record.label_conflict and record.duplicate_group_id
    }

    missing = sorted(eligible - assignments.keys())
    unexpected = sorted(set(assignments) - eligible)
    invalid_names = sorted(
        {split for split in assignments.values() if split not in SPLIT_NAMES}
    )
    checks.append(
        LeakageCheck(
            name="assignment_coverage",
            passed=not missing and not unexpected and not invalid_names,
            detail=(
                f"missing={len(missing)}, unexpected={len(unexpected)}, "
                f"invalid_split_names={len(invalid_names)}"
            ),
        )
    )

    counts = Counter(assignments.values())
    checks.append(
        LeakageCheck(
            name="non_empty_splits",
            passed=all(counts[split] > 0 for split in SPLIT_NAMES),
            detail=f"counts={dict(sorted(counts.items()))}",
        )
    )

    group_splits: dict[str, set[str]] = defaultdict(set)
    url_splits: dict[str, set[str]] = defaultdict(set)
    text_splits: dict[str, set[str]] = defaultdict(set)
    for index, split in assignments.items():
        record = records[index]
        group_splits[record.duplicate_group_id or ""].add(split)
        if record.url_group_id:
            url_splits[record.url_group_id].add(split)
        text_splits[normalize_for_comparison(record.text)].add(split)

    for name, mapping in (
        ("duplicate_component_leakage", group_splits),
        ("url_group_leakage", url_splits),
        ("exact_duplicate_leakage", text_splits),
    ):
        leaked = [key for key, splits in mapping.items() if len(splits) > 1]
        checks.append(
            LeakageCheck(
                name=name,
                passed=not leaked,
                detail=f"leaked_keys={len(leaked)}",
            )
        )

    leaked_pairs = 0
    for left, right in near_pairs:
        if left in assignments and right in assignments:
            if assignments[left] != assignments[right]:
                leaked_pairs += 1
    checks.append(
        LeakageCheck(
            name="near_duplicate_leakage",
            passed=leaked_pairs == 0,
            detail=f"leaked_pairs={leaked_pairs}",
        )
    )
    return checks


def make_split(
    records: list[CanonicalRecord],
    near_pairs: list[tuple[int, int]],
    config: SplitConfig | None = None,
) -> SplitResult:
    """Create a leakage-free group-aware split or raise SplitImpossibleError."""
    config = config or SplitConfig()
    ratio_total = config.train_ratio + config.validation_ratio + config.test_ratio
    if abs(ratio_total - 1.0) > 1e-9:
        raise SplitImpossibleError(f"split ratios must sum to 1, got {ratio_total}")

    eligible = [
        index
        for index, record in enumerate(records)
        if not record.label_conflict and record.duplicate_group_id
    ]
    quarantined_count = len(records) - len(eligible)
    if not eligible:
        raise SplitImpossibleError("no eligible records remain after quarantine")

    groups: dict[str, list[int]] = defaultdict(list)
    for index in eligible:
        groups[records[index].duplicate_group_id or ""].append(index)
    total_by_label = dict(
        sorted(Counter(records[index].target_label for index in eligible).items())
    )
    targets = _integer_targets(total_by_label, config)
    remaining = {split: dict(labels) for split, labels in targets.items()}

    rng = random.Random(config.seed)
    tie_order = rng.sample(SPLIT_NAMES, len(SPLIT_NAMES))
    ordered_groups = sorted(
        groups.items(), key=lambda item: (-len(item[1]), item[0])
    )

    assignments: dict[int, str] = {}
    for _group_id, members in ordered_groups:
        member_labels = Counter(records[index].target_label for index in members)
        scores: dict[str, tuple[int, int, int]] = {}
        for position, split in enumerate(tie_order):
            overlap = sum(
                min(count, remaining[split].get(label, 0))
                for label, count in member_labels.items()
            )
            spare = sum(remaining[split].values())
            scores[split] = (overlap, -spare, -position)
        chosen = max(scores, key=lambda split: scores[split])
        for index in members:
            assignments[index] = chosen
        for label, count in member_labels.items():
            remaining[chosen][label] = max(0, remaining[chosen].get(label, 0) - count)

    # If greedy stratification leaves an empty split, move the smallest
    # donor group rather than forcing an invalid split or changing labels.
    for split in SPLIT_NAMES:
        if split in assignments.values():
            continue
        group_split = {
            group_id: assignments[members[0]] for group_id, members in groups.items()
        }
        donor_group_counts = Counter(group_split.values())
        candidates = [
            group_id
            for group_id, donor_split in group_split.items()
            if donor_split != split and donor_group_counts[donor_split] > 1
        ]
        if not candidates:
            break
        chosen_group = min(candidates, key=lambda group_id: (len(groups[group_id]), group_id))
        for index in groups[chosen_group]:
            assignments[index] = split

    checks = validate_split(records, assignments, near_pairs)
    failed = [check.name for check in checks if not check.passed]
    if failed:
        raise SplitImpossibleError(
            "split rejected by leakage checks: " + ", ".join(failed)
        )

    updated = [
        record.with_split(assignments[index]) if index in assignments else record
        for index, record in enumerate(records)
    ]
    groups_by_split = Counter(
        records[members[0]].duplicate_group_id and assignments[members[0]]
        for members in groups.values()
    )
    record_counts = Counter(assignments.values())
    label_counts = {
        split: dict(
            sorted(
                Counter(
                    records[index].target_label
                    for index, assigned in assignments.items()
                    if assigned == split
                ).items()
            )
        )
        for split in SPLIT_NAMES
    }
    report = SplitReport(
        config=config.report_dict(),
        passed=True,
        eligible_record_count=len(eligible),
        quarantined_record_count=quarantined_count,
        group_count=len(groups),
        groups_by_split=dict(sorted(groups_by_split.items())),
        record_counts_by_split=dict(sorted(record_counts.items())),
        label_counts_by_split=label_counts,
        target_label_counts_by_split=targets,
        assignments={
            records[index].record_id: split
            for index, split in sorted(
                assignments.items(), key=lambda item: records[item[0]].record_id
            )
        },
        leakage_checks=checks,
    )
    return SplitResult(records=updated, report=report)
