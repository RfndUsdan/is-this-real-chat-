"""Stage 3 pipeline orchestration.

The orchestrator only produces report-safe artifacts. Raw text stays in the
in-memory canonical records and is never written by this module.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .data.dedup import (
    DedupConfig,
    DedupReport,
    attach_url_group_ids,
    build_dedup_result,
)
from .data.loader import load_mendeley_csv
from .data.schema import CanonicalRecord
from .data.split import SplitConfig, SplitReport, make_split
from .data.validation import ValidationReport, validate_dataset
from .data.workbook import WorkbookAudit, load_workbook_audit
from .preprocessing.text import PreprocessingConfig, TextPreprocessor


@dataclass(frozen=True, slots=True)
class PipelineResult:
    """All Stage 3 outputs; raw text remains only on ``records``."""

    validation: ValidationReport
    workbook: WorkbookAudit | None
    dedup: DedupReport | None
    split: SplitReport | None
    preprocessing: dict[str, Any] | None
    records: list[CanonicalRecord]
    stopped_stage: str | None

    @property
    def passed(self) -> bool:
        return (
            self.stopped_stage is None
            and self.validation.passed
            and self.dedup is not None
            and self.split is not None
            and self.split.passed
        )

    def report_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "stopped_stage": self.stopped_stage,
            "validation": self.validation.report_dict(),
            "workbook_audit": self.workbook.report_dict() if self.workbook else None,
            "dedup": self.dedup.report_dict() if self.dedup else None,
            "split": self.split.report_dict() if self.split else None,
            "preprocessing": self.preprocessing,
        }


def _preprocessing_summary(
    records: list[CanonicalRecord], config: PreprocessingConfig
) -> dict[str, Any]:
    preprocessor = TextPreprocessor(config)
    outputs = preprocessor.transform_records(records)
    raw_lengths = [len(record.text) for record in records]
    processed_lengths = [len(output.text) for output in outputs]
    count = len(records) or 1
    return {
        "config": config.report_dict(),
        "record_count": len(records),
        "mean_raw_length": round(sum(raw_lengths) / count, 2),
        "mean_processed_length": round(sum(processed_lengths) / count, 2),
        "records_shortened": sum(
            1 for raw, processed in zip(raw_lengths, processed_lengths) if processed < raw
        ),
        "tokenization_enabled": config.tokenize,
    }


def run_stage3_pipeline(
    csv_path: str | Path,
    *,
    workbook_path: str | Path | None = None,
    dedup_config: DedupConfig | None = None,
    split_config: SplitConfig | None = None,
    preprocessing_config: PreprocessingConfig | None = None,
) -> PipelineResult:
    """Run Stage 3 in order and stop on the first blocking check."""
    dataset = load_mendeley_csv(csv_path)
    validation = validate_dataset(dataset)
    if not validation.passed:
        return PipelineResult(
            validation=validation,
            workbook=None,
            dedup=None,
            split=None,
            preprocessing=None,
            records=[],
            stopped_stage="validation",
        )

    labels = {record.source_row: record.source_label for record in dataset.records}
    audit = (
        load_workbook_audit(workbook_path, source_labels=labels)
        if workbook_path
        else None
    )
    records = (
        attach_url_group_ids(dataset.records, audit) if audit else list(dataset.records)
    )
    dedup = build_dedup_result(records, dedup_config)
    split = make_split(dedup.records, dedup.near_duplicate_pairs, split_config)
    eligible = [record for record in split.records if record.split is not None]
    preprocessing = _preprocessing_summary(
        eligible, preprocessing_config or PreprocessingConfig()
    )
    return PipelineResult(
        validation=validation,
        workbook=audit,
        dedup=dedup.report,
        split=split.report,
        preprocessing=preprocessing,
        records=split.records,
        stopped_stage=None,
    )


def write_reports(result: PipelineResult, output_dir: str | Path) -> list[Path]:
    """Write report-safe JSON files to a local, ignored output directory."""
    target = Path(output_dir)
    target.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    artifacts: list[tuple[str, dict[str, Any]]] = [
        ("stage3-validation.json", result.validation.report_dict())
    ]
    if result.workbook:
        artifacts.append(("stage3-workbook-audit.json", result.workbook.report_dict()))
    if result.dedup:
        artifacts.append(("stage3-dedup.json", result.dedup.report_dict()))
        quarantine = {
            "reason_definition": "label_conflict_in_duplicate_component",
            "entries": [item.report_dict() for item in result.dedup.quarantine_entries],
        }
        artifacts.append(("stage3-quarantine.json", quarantine))
    if result.split:
        artifacts.append(("stage3-split.json", result.split.report_dict()))
    if result.preprocessing:
        artifacts.append(("stage3-preprocessing.json", result.preprocessing))
    artifacts.append(("stage3-summary.json", result.report_dict()))

    for name, payload in artifacts:
        path = target / name
        path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        written.append(path)
    return written
